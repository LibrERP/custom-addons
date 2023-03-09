#    Copyright (C) 2023 Didotech srl (<https://www.didotech.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"
    _description = "Invoice Line"
    _order = 'order_sequence ASC'

    order_sequence = fields.Integer(
        string='Sequenza ordine',
        compute='_compute_order_line',
        store=True,
    )

    @api.multi
    @api.depends('sale_line_ids')
    def _compute_order_line(self):
        for line in self:
            if line.sale_line_ids and line.sale_line_ids[0].sequence:
                line.order_sequence = line.sale_line_ids[0].sequence

