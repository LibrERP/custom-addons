# © 2022 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields, api, _, exceptions
from datetime import datetime


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    purchase_order_id = fields.Many2one(
        comodel_name="purchase.order", string="Purchase Order", required=False,
        ondelete='set null', readonly=True
    )

    @api.multi
    def action_create_purchase_order(self):
        pickings = self.browse(self.env.context['active_ids'])
        if pickings:
            new_orders = self.env['purchase.order']
            for picking in pickings:
                if picking.purchase_order_id:
                    raise exceptions.Warning(_(f'Order from transfer {picking.name} is already created.'))
                if not picking.partner_id:
                    raise exceptions.Warning(_(f'Partner from transfer {picking.name} is not specified.'))

                order_values = {
                    'partner_id': picking.partner_id.id,
                    'partner_ref': picking.name,
                    'order_line': []
                }

                new_order = self.env['purchase.order'].create(order_values)
                picking.purchase_order_id = new_order.id

                for move in picking.move_ids_without_package:
                    line_values = {
                        'product_id': move.product_id.id,
                        'name': move.product_id.name,
                        'product_qty': move.product_qty,
                        'date_planned': datetime.now(),
                        'product_uom': move.product_uom.id,
                        'price_unit': 0,
                        'order_id': new_order.id
                    }
                    order_line = self.env['purchase.order.line'].create(line_values)
                    move.purchase_line_id = order_line.id

                new_orders += new_order
            if new_orders:
                return {
                    'type': 'ir.actions.act_window',
                    'name': _('New Orders'),
                    'res_model': 'purchase.order',
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'view_id': False,
                    'target': 'current',
                    'res_id': False,
                    "domain": [('id', 'in', new_orders.ids)]
                }
