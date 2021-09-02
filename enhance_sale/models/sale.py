# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2020-2020 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2020-09-04
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
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.one
    @api.depends('picking_ids.date_done')
    def _compute_delivered(self):
        for order in self:
            delivered = True if len(order.picking_ids)> 0 else False
            for picking in order.picking_ids:
                delivered &= (picking.state == 'done')
            order.delivered = delivered

    delivered = fields.Boolean("Delivered Order", compute='_compute_delivered', help="Completed delivery of this order.")


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def show_transport_documents(self):
        """
            Shows TD for each sale order line.
        """
        ret = {}
        tdEntity = 'stock.picking.package.preparation'
        tdEntity_type = self.env[tdEntity]
        picking_ids = self.env['stock.picking']
        transport_document_ids = tdEntity_type
        for line in self:
            for move in line.move_ids:
                picking_ids += move.picking_id
        for picking_id in picking_ids:
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

