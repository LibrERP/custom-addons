# © 2021 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, api


class WizardImportFatturapa(models.TransientModel):
    _inherit = 'wizard.link.to.invoice.line'

    @api.multi
    def link(self):
        result = super().link()
        self.invoice_id.e_invoice_received_date = self.wizard_id.attachment_id.e_invoice_received_date.date()
        return result
