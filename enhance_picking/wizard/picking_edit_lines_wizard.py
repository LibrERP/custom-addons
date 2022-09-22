# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import clean_context


class PickingEdit(models.TransientModel):
    _name = 'stock.picking.edit'
    _description = 'Picking Edit'

    line_ids = fields.One2many('stock.picking.edit.line', 'picking_edit_id')

    @api.multi
    def update_lines(self, *args, **kwargs):
        print(self)

    @api.multi
    def write(self, values):
        if self.env.context.get('create_from'):
            for i, line in enumerate(self.line_ids):
                line_ids = values.get('line_ids')
                if line_ids:
                    if line_ids[i][2]:
                        if line_ids[i][2].get('quantity_done') > line.product_uom_qty:
                            raise UserError('Inputted amount of quantity done is greater than product quantity')

                        move_line_vals = line.move_id._prepare_move_line_vals()
                        #search for any move lines already present in there
                        move_lines = self.env['stock.move.line'].search([('move_id', '=', move_line_vals['move_id']), ('product_uom_qty', '=', 0)])
                        if move_lines:
                            #Update the first one because there isn't a rule to know which to update
                            move_lines[0].update({'qty_done': line_ids[i][2]['quantity_done']})
                        else:
                            move_line_vals['qty_done'] = line_ids[i][2]['quantity_done']
                            self.env['stock.move.line'].create(move_line_vals)

        return {'type': 'ir.actions.act_window_close'}


class PickingEditLine(models.TransientModel):
    _name = 'stock.picking.edit.line'
    _description = 'Picking Edit Lines'

    picking_edit_id = fields.Many2one('stock.picking.edit')
    move_id = fields.Many2one('stock.move')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    product_uom_qty = fields.Float()
    reserved_availability = fields.Float()
    quantity_done = fields.Float()
    product_uom = fields.Many2one('uom.uom', string='Unity of measure')

    @api.onchange('quantity_done')
    def _onchange_quantity_done(self):
        if self.quantity_done > self.product_uom_qty:
            return {
                'warning': {
                    'title': _('Warning'),
                    'message': _(
                        'Inputted amount of quantity done is greater than product quantity'
                    )
                }
            }