# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models


class StockDeliveryNoteInvoiceWizard(models.TransientModel):
    _inherit = "stock.delivery.note.invoice.wizard"

    journal_id = fields.Many2one(
        comodel_name='account.journal', string='Journal',
        domain=[('type', '=', 'sale')],
        required=True
    )

    def create_invoices(self):
        if self.journal_id:
            ctx = dict(self._context)
            ctx['default_journal_id'] = self.journal_id.id
            return super(StockDeliveryNoteInvoiceWizard, self.with_context(ctx)).create_invoices()
        else:
            return super(StockDeliveryNoteInvoiceWizard, self).create_invoices()
