# Copyright 2021 Andrei Levin - Didotech srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.model
    def invoice_line_move_line_get(self):
        """Correct global rounding move lines (add taxes)"""
        res = super().invoice_line_move_line_get()

        for line in res:
            if line['type'] == 'global_rounding' and 'tax_ids' not in line:
                line['tax_ids'] = [(4, self.env.user.company_id.arrotondamenti_tax_id.id, None)]

        return res
