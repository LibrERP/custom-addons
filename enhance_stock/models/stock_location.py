# -*- encoding: utf-8 -*-
##############################################################################
#
#    Created on : 2022-07-27
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


class StockLocation(models.Model):
    _inherit = "stock.location"

    @api.multi
    def action_product_on_location(self):
        """
            Returns an action that displays existing products
            stored on active location.
        """
        action = False
        if ('location_id' in self._context):
            locationId = self._context['location_id']
            criteria = [
                ('location_id', '=', locationId),
                ]
            quant_ids = self.env['stock.quant'].search(criteria)
            product_ids = quant_ids.mapped("product_id")
            if product_ids:
                action = self.env.ref('product.product_normal_action').read()[0]
                action['domain'] = [('id', 'in', product_ids.ids)]
        return action
