# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.onchange('move_ids_without_package.tracking')
    def onchange_tracking(self):
        pass


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.onchange('tracking')
    def onchange_tracking(self):
        tracking = self.tracking
        if len(self.move_line_ids) > 1:
            for move_line in self.move_line_ids.filtered(lambda sml: sml.reserved_uom_qty == 0):
                move_line.unlink()

            self.tracking = tracking

        if len(self.move_line_ids) == 1:
            if self.tracking == 'lot':
                move_line = self.move_line_ids[0].copy()
                new_line = move_line
                new_line.reserved_uom_qty = 0
                new_line.qty_done = self.move_line_ids[0].reserved_uom_qty
                new_line.lot_name = self.env['stock.move.line'].get_unique_serial_number()
            elif self.tracking == 'serial':
                for count in range(int(self.move_line_ids[0].reserved_uom_qty)):
                    move_line = self.move_line_ids[0].copy()
                    new_line = move_line
                    new_line.reserved_uom_qty = 0
                    new_line.qty_done = 1
                    new_line.lot_name = self.env['stock.move.line'].get_unique_serial_number()


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def get_unique_serial_number(self):
        return self.env['ir.sequence'].next_by_code('stock.lot')

    @api.model_create_multi
    def create(self, values):
        new_values = []
        for value in values:
            product = self.env['product.product'].browse(value['product_id'])
            if product.tracking == 'lot' and 'lot_name' not in value:
                new_value = value.copy()
                new_value.update({
                    'reserved_uom_qty': 0,
                    'qty_done': int(value['reserved_uom_qty']),
                    'lot_name': self.get_unique_serial_number()
                })
                new_values.append(new_value)
            elif product.tracking == 'serial' and 'lot_name' not in value:
                for count in range(int(value['reserved_uom_qty'])):
                    new_value = value.copy()
                    new_value.update({
                        'reserved_uom_qty': 0,
                        'qty_done': 1,
                        'lot_name': self.get_unique_serial_number()
                    })
                    new_values.append(new_value)

        values += new_values
        return super().create(values)
