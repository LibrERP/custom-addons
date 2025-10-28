# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        invoice_values = super()._prepare_invoice()

        if self._context.get('default_journal_id'):
            invoice_values['journal_id'] = self._context['default_journal_id']

        return invoice_values
