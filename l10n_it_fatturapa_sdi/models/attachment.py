# © 2024-2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models
from odoo.addons.l10n_it_fatturapa_sdi.models.sdi_lib import E_INVOICE_STATE


class FatturapaAttachmentOut(models.Model):
    _inherit = "fatturapa.attachment.out"
    _description = "Generic class for SDI communication"

    sdi_fname = fields.Text('SDI full file path')
    sdi_id = fields.Char('ID SdI', size=12)
    sdi_state = fields.Selection(E_INVOICE_STATE, 'SdI State', readonly=True, required=False)
    sdi_download_date = fields.Date('Download date')


class FatturapaAttachmentIn(models.Model):
    _inherit = "fatturapa.attachment.in"

    sdi_id = fields.Char('IdSdi', readonly=True)
    office_code = fields.Char('Office Code', readonly=True)
