# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class WizardLinkToInvoice(models.TransientModel):
    _inherit = "wizard.link.to.invoice"

    partner_id = fields.Many2one(comodel_name='res.partner', related='attachment_id.xml_supplier_id')

