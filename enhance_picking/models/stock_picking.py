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


