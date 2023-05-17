# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
from odoo.tools import float_compare
from odoo.exceptions import ValidationError, UserError

import itertools


class MassiveDdtCreation(models.TransientModel):
    _name = 'wizard.massive.ddt.creation'

    type_ddt = fields.Many2one(
        'stock.ddt.type',
        string='Required TD Type',
        required=True,
        index=True,
    )
    line_ids = fields.One2many('wizard.massive.ddt.creation.line', 'parent_id')

    def open_wizard(self):
        return {
            'name': _('Massive DDT creation'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            "view_type": "form",
            'res_model': 'wizard.massive.ddt.creation',
            'target': 'new',
            'view_id': self.env.ref
            ('massive_ddt_creation.view_massive_ddt_creation').id,
            'context': self.env.context,
        }

    @api.model
    def default_get(self, fields):
        context = self.env.context
        ddt_lines = []
        picking_model = self.env['stock.picking']
        have_same_term = self.env['ir.config_parameter'].sudo().get_param('massive_ddt_creation.massive_ddt_same_term')
        if context.get('active_model') == 'stock.picking':
            pickings = picking_model.browse(context['active_ids'])
            # Check if pickings have the same partner
            if len(set(map(lambda p: p.partner_id.id, pickings))) > 1:
                raise ValidationError(_('Select pickings with the same partner'))
            # Check if all selected pickings are in state `assigned`
            if len(pickings.filtered(lambda p: p.state != 'assigned')) > 0:
                raise ValidationError(_('Select only pickings in assigned state'))
        elif context.get('active_model') == 'sale.order':
            sorders = self.env['sale.order'].browse(context['active_ids'])
            pickings = sorders.mapped('picking_ids').filtered(lambda p: p.state == 'assigned' and not p.ddt_ids)
            # To create DDTs the partner should be the same for the selected sale orders
            if len(set(map(lambda p: p.partner_id.id, pickings))) > 1:
                raise ValidationError(_('Select pickings with the same partner'))
            if have_same_term and len(set(map(lambda p: p.payment_term_id.id, sorders))) > 1:
                raise ValidationError(_('Selected orders must have the same payment term!'))
        else:
            raise ValidationError('Not supported')  # should never happen, only fixes python linter

        for picking in pickings:
            # We don't want pickings that already have a ddt attached
            if picking.ddt_ids:
                continue
            for move in picking.move_lines:
                available_quantity_quant = move.product_id._compute_quantities_dict(None, None, None)[
                    move.product_id.id].get('qty_available')
                hide_lines = self.env['ir.config_parameter'].sudo().get_param(
                    'massive_ddt_creation.hide_lines_not_ready')
                if hide_lines and move.reserved_availability == 0:
                    continue

                ddt_lines.append((0, 0, {
                    'move_id': move.id,
                    'picking_id': picking.id,
                    'product_id': move.product_id.id,
                    'product_uom_qty': move.product_uom_qty,
                    'reserved_availability': move.reserved_availability,
                    'quantity_done': move.reserved_availability,
                    'qty_in_stock': available_quantity_quant,
                    'product_uom': move.product_uom.id
                }))
        return {'line_ids': ddt_lines}

    @api.multi
    def pre_validate(self):
        # order by planned date
        lines = self.line_ids.sorted(key=lambda p: p.picking_id.scheduled_date)
        pickings_to_include = self.env['stock.picking']
        allow_more_qty = self.env['ir.config_parameter'].sudo().get_param(
            'massive_ddt_creation.allow_more_qty')
        allow_manual_complete_td = self.env['ir.config_parameter'].sudo().get_param(
            'massive_ddt_creation.allow_manual_complete_td')
        # process pickings and validate
        for picking_id, moves in itertools.groupby(lines, lambda p: p.picking_id.id):
            moves_list = list(moves)
            for line in moves_list:
                if line.quantity_done > line.product_uom_qty:
                    if not allow_more_qty:
                        raise UserError(_(
                            f'Inputted amount of quantity done for {line.product_id.name} is greater than requested quantity'))
                # manipulate move lines
                move_line_vals = line.move_id._prepare_move_line_vals()
                # search for any move lines already present in there
                move_lines = self.env['stock.move.line'].search([('move_id', '=', move_line_vals['move_id'])])
                if move_lines:
                    # Update the first one because there isn't a rule to know which to update
                    move_lines[0].update({'qty_done': line.quantity_done})
                else:
                    move_line_vals['qty_done'] = line.quantity_done
                    self.env['stock.move.line'].create(move_line_vals)

            # Do nothing because no action was done in this picking
            if len(list(filter(lambda m: m.quantity_done == 0, moves_list))) == len(moves_list):
                continue

            pick_id = self.env['stock.picking'].browse(picking_id)
            # This will create a backorder for move lines that haven't been completed
            if not allow_manual_complete_td:
                pick_id.action_done()
            else:
                pick_id.action_assign()
                pick_id.state = 'assigned'
            pickings_to_include += pick_id
        return pickings_to_include

    @api.multi
    def validate(self):
        pickings_to_include = self.pre_validate()
        # Create ddt using sale order data
        if pickings_to_include:
            allow_manual_complete_td = self.env['ir.config_parameter'].sudo().get_param(
                'massive_ddt_creation.allow_manual_complete_td')
            ddtType = self.env['stock.picking.package.preparation']
            ddt_wizard = self.env['ddt.from.pickings'].create(
                {'picking_ids': [(6, 0, pickings_to_include.ids)], 'type_ddt': self.type_ddt.id})
            ddt_action = ddt_wizard.create_ddt()
            ddt_id = ddtType.browse(ddt_action.get('res_id'))
            if ddt_id:
                if self.type_ddt:
                    values={
                        'carriage_condition_id': self.type_ddt.default_carriage_condition_id.id or False,
                        'goods_description_id': self.type_ddt.default_goods_description_id.id or False,
                        'transportation_reason_id': self.type_ddt.default_transportation_reason_id.id or False,
                        'transportation_method_id': self.type_ddt.default_transportation_method_id.id or False,
                    }
                    ddt_id.write(values)
                if not allow_manual_complete_td:
                    ddt_id.set_done()
                else:
                    ddt_id.action_put_in_pack()
            return ddt_action

        return {'type': 'ir.actions.act_window_close'} # If no picking was processed just close wizard


class MassiveDdtCreationLine(models.TransientModel):
    _name = 'wizard.massive.ddt.creation.line'

    parent_id = fields.Many2one(
        'wizard.massive.ddt.creation',
        index=True,
    )
    move_id = fields.Many2one(
        'stock.move',
        index=True,
    )
    picking_id = fields.Many2one(
        'stock.picking',
        index=True,
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        index=True,
    )
    product_uom_qty = fields.Float(
        'Quantity to deliver',
        digits=dp.get_precision('Product Unit of Measure'),
    )
    reserved_availability = fields.Float(digits=dp.get_precision('Product Unit of Measure'))
    quantity_done = fields.Float(digits=dp.get_precision('Product Unit of Measure'))
    qty_in_stock = fields.Float()
    product_uom = fields.Many2one(
        'uom.uom',
        string='Unity of measure',
        index=True,
    )
