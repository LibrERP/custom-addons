# © 2022 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _


class StockPickingPackagePreparationLine(models.Model):
    _inherit = 'stock.picking.package.preparation.line'
    _order = 'sale_order_name ASC, sale_order_line_sequence ASC, id DESC'

    sale_order_name = fields.Char(string="Sale Order Name")
    sale_order_line_sequence = fields.Integer(string="Order Line Sequence")

    @api.model_create_multi
    def create(self, values):
        for values_set in values:
            move = self.env['stock.move'].browse(values_set['move_id'])
            values_set.update({
                'sale_order_name': move.sale_line_id.order_id.name,
                'sale_order_line_sequence': move.sale_line_id.sequence
            })
        return super().create(values)
