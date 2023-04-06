# © 2008-2014 Alistek
# © 2016-2018 Savoir-faire Linux
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# © 2022 Didotech srl (https://www.didotech.com)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl).
import os
import logging
from odoo import models, fields, api, tools, _
from odoo.exceptions import ValidationError
from tempfile import NamedTemporaryFile
from .subprocess import run_subprocess
from odoo.addons.report_aeroo.models.ir_actions_report import IrActionsReport as OriginelIrActionsReport

_logger = logging.getLogger(__name__)


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def _convert_aeroo_report(self, output, output_format):
        """Convert a generated aeroo report to the output format.

        :param string output: the aeroo data to convert.
        :return: the content of the generated report
        :rtype: bytes
        """
        # output_dummy = super()._convert_aeroo_report(output, output_format)

        in_format = self.aeroo_in_format

        temp_file = generate_temporary_file(in_format, output)
        filedir, filename = os.path.split(temp_file.name)

        libreoffice_location = self._get_aeroo_config_parameter('libreoffice_location')

        cmd = libreoffice_location.split(' ') + [
            "--headless",
            "--convert-to", output_format,
            "--outdir", filedir, temp_file.name
        ]

        timeout = self._get_aeroo_libreoffice_timeout()

        try:
            run_subprocess(cmd, timeout)
        except Exception as exc:
            os.remove(temp_file.name)
            _logger.info('Eccezione {nome}'.format(nome=exec))
            raise ValidationError(
                _('Could not generate the report %(report)s '
                  'using the format %(output_format)s. '
                  '%(error)s') % {
                    'report': self.name,
                    'output_format': output_format,
                    'error': exc,
                })

        output_file = temp_file.name[:-3] + output_format
        with open(output_file, 'rb') as f:
            output = f.read()

        os.remove(temp_file.name)
        os.remove(output_file)

        return output


def generate_temporary_file(format, data=None):
    """Generate a temporary file containing the given data.

    :param string format: the extension of the file to create
    :param bytes data: the data to write in the file
    """
    temp_file = NamedTemporaryFile(suffix='.%s' % format, delete=False)
    temp_file.close()
    if data is not None:
        with open(temp_file.name, 'wb') as f:
            f.write(data)
    # _logger.info('file generato {nome}'.format(nome=temp_file))
    return temp_file


OriginelIrActionsReport._convert_aeroo_report = IrActionsReport._convert_aeroo_report

