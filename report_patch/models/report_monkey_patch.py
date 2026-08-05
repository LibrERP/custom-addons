# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.addons.base.models.ir_actions_report import IrActionsReport
from collections import OrderedDict
from PIL import Image, ImageFile
import io
import logging

from odoo.exceptions import UserError
from odoo.tools.pdf import PdfFileWriter, PdfFileReader, PdfReadError
from odoo import _

_logger = logging.getLogger(__name__)


# Save original method to reuse everything else
_original__pdf_prepare_streams = IrActionsReport._render_qweb_pdf_prepare_streams


def patched_render_qweb_pdf_prepare_streams(self, report_ref, data, res_ids=None):
    # NOTE:
    # This monkey patch is based on Odoo 18.x implementation of
    # _render_qweb_pdf_prepare_streams().
    #
    # It only changes one behavior:
    # when the generated PDF contains no /Outlines object,
    # fall back to rendering documents individually instead of
    # returning the merged PDF.
    #
    # Remove this patch once Odoo fixes the issue upstream.

    def _render_individually():
        for res_id in res_ids_wo_stream:
            individual = self.with_context(
                _pdf_split_fallback=True
            )._render_qweb_pdf_prepare_streams(
                report_ref=report_ref,
                data=data,
                res_ids=[res_id],
            )
            collected_streams[res_id]['stream'] = individual[res_id]['stream']
        return collected_streams

    if self.env.context.get("_pdf_split_fallback"):
        return _original__pdf_prepare_streams(self, report_ref, data, res_ids)

    if not data:
        data = {}
    data.setdefault('report_type', 'pdf')

    # access the report details with sudo() but evaluation context as current user
    report_sudo = self._get_report(report_ref)
    has_duplicated_ids = res_ids and len(res_ids) != len(set(res_ids))

    collected_streams = OrderedDict()

    # Fetch the existing attachments from the database for later use.
    # Reload the stream from the attachment in case of 'attachment_use'.
    if res_ids:
        records = self.env[report_sudo.model].browse(res_ids)
        for record in records:
            res_id = record.id
            if res_id in collected_streams:
                continue

            stream = None
            attachment = None
            if not has_duplicated_ids and report_sudo.attachment and not self._context.get("report_pdf_no_attachment"):
                attachment = report_sudo.retrieve_attachment(record)

                # Extract the stream from the attachment.
                if attachment and report_sudo.attachment_use:
                    stream = io.BytesIO(attachment.raw)

                    # Ensure the stream can be saved in Image.
                    if attachment.mimetype.startswith('image'):
                        img = Image.open(stream)
                        new_stream = io.BytesIO()
                        img.convert("RGB").save(new_stream, format="pdf")
                        stream.close()
                        stream = new_stream

            collected_streams[res_id] = {
                'stream': stream,
                'attachment': attachment,
            }

    # Call 'wkhtmltopdf' to generate the missing streams.
    res_ids_wo_stream = [res_id for res_id, stream_data in collected_streams.items() if not stream_data['stream']]
    all_res_ids_wo_stream = res_ids if has_duplicated_ids else res_ids_wo_stream
    is_whtmltopdf_needed = not res_ids or res_ids_wo_stream

    if is_whtmltopdf_needed:

        if self.get_wkhtmltopdf_state() == 'install':
            # wkhtmltopdf is not installed
            # the call should be catched before (cf /report/check_wkhtmltopdf) but
            # if get_pdf is called manually (email template), the check could be
            # bypassed
            raise UserError(_("Unable to find Wkhtmltopdf on this system. The PDF can not be created."))

        # Disable the debug mode in the PDF rendering in order to not split the assets bundle
        # into separated files to load. This is done because of an issue in wkhtmltopdf
        # failing to load the CSS/Javascript resources in time.
        # Without this, the header/footer of the reports randomly disappear
        # because the resources files are not loaded in time.
        # https://github.com/wkhtmltopdf/wkhtmltopdf/issues/2083
        additional_context = {'debug': False}
        data.setdefault("debug", False)

        html = self.with_context(**additional_context)._render_qweb_html(report_ref, all_res_ids_wo_stream, data=data)[
            0]

        bodies, html_ids, header, footer, specific_paperformat_args = report_sudo.with_context(
            **additional_context)._prepare_html(html, report_model=report_sudo.model)

        if not has_duplicated_ids and report_sudo.attachment and set(res_ids_wo_stream) != set(html_ids):
            raise UserError(_(
                "Report template “%s” has an issue, please contact your administrator. \n\n"
                "Cannot separate file to save as attachment because the report's template does not contain the"
                " attributes 'data-oe-model' and 'data-oe-id' as part of the div with 'article' classname.",
                report_sudo.name,
            ))

        pdf_content = self._run_wkhtmltopdf(
            bodies,
            report_ref=report_ref,
            header=header,
            footer=footer,
            landscape=self._context.get('landscape'),
            specific_paperformat_args=specific_paperformat_args,
            set_viewport_size=self._context.get('set_viewport_size'),
        )

        pdf_content_stream = io.BytesIO(pdf_content)

        # Printing a PDF report without any records. The content could be returned directly.
        if has_duplicated_ids or not res_ids:
            return {
                False: {
                    'stream': pdf_content_stream,
                    'attachment': None,
                }
            }

        # Split the pdf for each record using the PDF outlines.

        # Only one record: append the whole PDF.
        if len(res_ids_wo_stream) == 1:
            collected_streams[res_ids_wo_stream[0]]['stream'] = pdf_content_stream
            return collected_streams

        # In case of multiple docs, we need to split the pdf according the records.
        # In the simplest case of 1 res_id == 1 page, we use the PDFReader to print the
        # pages one by one.
        html_ids_wo_none = [x for x in html_ids if x]
        reader = PdfFileReader(pdf_content_stream)
        if reader.numPages == len(res_ids_wo_stream):
            for i in range(reader.numPages):
                attachment_writer = PdfFileWriter()
                attachment_writer.addPage(reader.getPage(i))
                stream = io.BytesIO()
                attachment_writer.write(stream)
                collected_streams[res_ids_wo_stream[i]]['stream'] = stream
            return collected_streams

        # In cases where the number of res_ids != the number of pages,
        # we split the pdf based on top outlines computed by wkhtmltopdf.
        # An outline is a <h?> html tag found on the document. To retrieve this table,
        # we look on the pdf structure using pypdf to compute the outlines_pages from
        # the top level heading in /Outlines.
        if len(res_ids_wo_stream) > 1 and set(res_ids_wo_stream) == set(html_ids_wo_none):
            root = reader.trailer['/Root']
            has_valid_outlines = '/Outlines' in root and '/First' in root['/Outlines']
            if not has_valid_outlines:
                _logger.warning(
                    "PDF report %s contains no valid outlines. "
                    "Falling back to individual rendering.",
                    report_ref,
                )
                return _render_individually()

            outlines_pages = []
            node = root['/Outlines']['/First']
            while True:
                outlines_pages.append(root['/Dests'][node['/Dest']][0])
                if '/Next' not in node:
                    break
                node = node['/Next']
            outlines_pages = sorted(set(outlines_pages))

            # The number of outlines must be equal to the number of records to be able to split the document.
            has_same_number_of_outlines = len(outlines_pages) == len(res_ids_wo_stream)

            # There should be a top-level heading on first page
            has_top_level_heading = outlines_pages[0] == 0

            if has_same_number_of_outlines and has_top_level_heading:
                # Split the PDF according to outlines.
                for i, num in enumerate(outlines_pages):
                    to = outlines_pages[i + 1] if i + 1 < len(outlines_pages) else reader.numPages
                    attachment_writer = PdfFileWriter()
                    for j in range(num, to):
                        attachment_writer.addPage(reader.getPage(j))
                    stream = io.BytesIO()
                    attachment_writer.write(stream)
                    collected_streams[res_ids_wo_stream[i]]['stream'] = stream
                return collected_streams
            else:
                return _render_individually()

        collected_streams[False] = {'stream': pdf_content_stream, 'attachment': None}

    return collected_streams


IrActionsReport._render_qweb_pdf_prepare_streams = patched_render_qweb_pdf_prepare_streams
