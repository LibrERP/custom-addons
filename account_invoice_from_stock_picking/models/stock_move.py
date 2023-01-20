# © 2022-2023 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models, api


class StockMove(models.Model):
    _name = 'stock.move'
    _inherit = [
        _name,
        "stock.invoice.state.mixin",
    ]

    invoiced = fields.Boolean()
    invoice_line_ids = fields.Many2many('account.invoice.line')
    qty_invoiced = fields.Float(default=0)
