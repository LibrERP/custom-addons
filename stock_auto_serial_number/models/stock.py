# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.onchange('tracking')
    def onchange_tracking(self):
        tracking = self.tracking
        if len(self.move_line_ids) > 1:
            for move_line in self.move_line_ids.filtered(lambda sml: sml.reserved_uom_qty == 0):
                self.picking_id.move_line_ids = [Command.unlink(move_line.id)]
                move_line.unlink()

            self.move_line_ids.clear_caches()
            self.picking_id.clear_caches()
            self.tracking = tracking

        if len(self.move_line_ids) == 1:
            move_line_model = self.env['stock.move.line']
            new_line = self.env['stock.move.line']
            move_line = self.move_line_ids[0]
            if self.tracking == 'lot':
                new_values = {
                    'company_id': move_line.company_id.id,
                    'location_dest_id': move_line.location_dest_id.id,
                    'location_id': move_line.location_id.id,
                    'lot_id': False,
                    'lot_name': move_line_model.get_unique_serial_number(),
                    'move_id': move_line.move_id.id,
                    'package_id': False,
                    'package_level_id': False,
                    'picking_id': move_line.picking_id.ids[0],  # This is correct as id con be shown as NewId
                    'product_id': move_line.product_id.id,
                    'product_uom_id': move_line.product_uom_id.id,
                    'qty_done': move_line.reserved_uom_qty
                }
                new_line += move_line_model.create(new_values)

            elif self.tracking == 'serial':
                for count in range(int(self.move_line_ids[0].reserved_uom_qty)):
                    new_values = {
                        'company_id': move_line.company_id.id,
                        'location_dest_id': move_line.location_dest_id.id,
                        'location_id': move_line.location_id.id,
                        'lot_id': False,
                        'lot_name': move_line_model.get_unique_serial_number(),
                        'move_id': move_line.move_id.id,
                        'package_id': False,
                        'package_level_id': False,
                        'picking_id': move_line.picking_id.ids[0],  # This is correct as id con be shown as NewId
                        'product_id': move_line.product_id.id,
                        'product_uom_id': move_line.product_uom_id.id,
                        'qty_done': 1
                    }
                    new_line += move_line_model.create(new_values)


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def get_unique_serial_number(self):
        return self.env['ir.sequence'].next_by_code('stock.lot')

    @api.model_create_multi
    def create(self, values):
        new_values = []
        for value in values:
            move = self.env['stock.move'].browse(value['move_id'])
            if move.picking_id and move.picking_id.picking_type_code == 'incoming':
                product = self.env['product.product'].browse(value['product_id'])
                quantity = value.get('reserved_uom_qty', False) or value.get('qty_done')
                if product.tracking == 'lot' and 'lot_name' not in value and 'lot_id' not in value:
                    new_value = value.copy()
                    new_value.update({
                        'reserved_uom_qty': 0,
                        'qty_done': int(quantity),
                        'lot_name': self.get_unique_serial_number()
                    })
                    new_values.append(new_value)
                elif product.tracking == 'serial' and 'lot_name' not in value and 'lot_id' not in value:
                    for count in range(int(quantity)):
                        new_value = value.copy()
                        new_value.update({
                            'reserved_uom_qty': 0,
                            'qty_done': 1,
                            'lot_name': self.get_unique_serial_number()
                        })
                        new_values.append(new_value)

        values += new_values
        return super().create(values)
