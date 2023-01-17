# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2020-2021 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2021-00-11
#    Author : Fabio Colognesi
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


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.one
    def _count_tds(self):
        self.delivery_count = len(self.ddt_ids)

    delivery_count = fields.Integer("Deliveries", compute=_count_tds)

    def show_transport_documents(self):
        """
            Shows TD for each sale order line.
        """
        ret = {}
        tdEntity = 'stock.picking.package.preparation'
        tdEntity_type = self.env[tdEntity]
        transport_document_ids = tdEntity_type
        for picking_id in self:
            for ddt_id in picking_id.ddt_ids:
                transport_document_ids += ddt_id
        if transport_document_ids:
            ret = {
                'type': 'ir.actions.act_window',
                'name': _(tdEntity_type._description),
                'res_model': tdEntity,
                'view_mode': 'tree,form',
                'view_type': 'form',
                'domain': [('id', 'in', transport_document_ids.ids)],
                'target': 'current',
            }
        return ret

    @api.multi
    def prepare_validation(self):
        picking_edit = self.env['stock.picking.edit']
        picking_edit_line = self.env['stock.picking.edit.line']
        values = {}
        picking_edit_id = picking_edit.create({})
        for move in self.move_lines:
            values.update({
                'product_id': move.product_id.id,
                'product_uom_qty': move.product_uom_qty,
                'reserved_availability': move.reserved_availability,
                'quantity_done': move.reserved_availability,
                'product_uom': move.product_uom.id,
                'picking_edit_id': picking_edit_id.id,
                'move_id': move.id
            })
            picking_edit_line.create(values)

        action = self.env.ref('enhance_picking.action_stock_picking_edit_form').read()[0]
        action['res_id'] = picking_edit_id.id
        return action

    @api.model
    def check_availability(self):
        """
            Re-evaluates ram materials availability on stock.picking
        """
        criteria = [('state', 'in', ['confirmed','waiting'])]
        picking_ids = self.search(criteria)
        for picking_id in picking_ids:
            picking_id.action_assign()
