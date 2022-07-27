# -*- encoding: utf-8 -*-
##############################################################################
#
#    Created on : 2022-07-07
#    Author : Fabio Colognesi
#    Copyright: Didotech srl 2020 - 2022
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, models, fields, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('picking_ids','partner_id')
    def _compute_waiting_picking_ids(self):
        for order_id in self:
            partner_id = order_id.partner_id
            if partner_id.parent_id:
                partner_id = partner_id.parent_id
            criteria = [
                ('state', 'in', ['assigned','partial_available']),
                '|', 
                ('partner_id', '=', partner_id.id),
                ('partner_id', 'in', partner_id.child_ids.ids),
                ]
            pickings = self.env['stock.picking'].search(criteria)
            pickings -= order_id.picking_ids
            order_id.not_yet_delivered_count = len(pickings)
    
    not_yet_delivered_count = fields.Integer(
        string='Waiting Delivery Orders',
        compute='_compute_waiting_picking_ids')

    @api.multi
    def action_view_to_delivery(self):
        '''
        This function returns an action that display existing delivery orders
        of given sales order ids. It can either be a in a list or in a form
        view, if there is only one delivery order to show.
        '''
        action = self.env.ref('stock.action_picking_tree_all').read()[0]

        partner_id = self.partner_id
        if partner_id.parent_id:
            partner_id = partner_id.parent_id
        criteria = [
            ('state', 'in', ['assigned','partial_available']),
            '|', 
            ('partner_id', '=', partner_id.id),
            ('partner_id', 'in', partner_id.child_ids.ids),
            ]
        pickings = self.env['stock.picking'].search(criteria)

        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids)]
        elif pickings:
            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = pickings.id
        return action
