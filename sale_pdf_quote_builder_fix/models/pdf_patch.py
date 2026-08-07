# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import logging
import odoo.tools.pdf as odoo_pdf

NameObject = odoo_pdf.generic.NameObject
DictionaryObject = odoo_pdf.generic.DictionaryObject
ArrayObject = odoo_pdf.generic.ArrayObject

_logger = logging.getLogger(__name__)

# Keep original reference
_original_fill = odoo_pdf.fill_form_fields_pdf


def _ensure_acroform_from_pages(writer):
    """
    If writer lost /AcroForm (which happens when pages are concatenated),
    rebuild a minimal one from page widget annotations.
    """

    if writer._root_object.get("/AcroForm"):
        return

    fields = ArrayObject()

    for page in writer.pages:
        annots = page.get("/Annots")
        if not annots:
            continue

        for annot in annots:
            obj = annot.get_object()
            if obj.get("/Subtype") == "/Widget" and obj.get("/T"):
                fields.append(annot)

    if not fields:
        return

    acroform = DictionaryObject()
    acroform[NameObject("/Fields")] = fields

    writer._root_object[NameObject("/AcroForm")] = acroform

    _logger.debug("Reconstructed /AcroForm from widget annotations.")


def safe_fill_form_fields_pdf(writer, form_fields=None):
    if not form_fields:
        return

    _ensure_acroform_from_pages(writer)

    try:
        root = getattr(writer, "_root_object", None)
        acroform = root.get("/AcroForm") if root else None
        has_fields = (
            acroform
            and acroform.get("/Fields")
            and len(acroform.get("/Fields")) > 0
        )
    except Exception:
        has_fields = False

    if not has_fields:
        _logger.debug("Skipping PDF form fill: no AcroForm fields present.")
        return

    for page in writer.pages:
        try:
            writer.update_page_form_field_values(page, form_fields)
        except Exception:
            # DO NOT depend on pypdf import
            _logger.warning(
                "Error while updating form fields. Skipping.",
                exc_info=True,
            )
            return


odoo_pdf.fill_form_fields_pdf = safe_fill_form_fields_pdf
