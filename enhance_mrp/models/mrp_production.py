# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2020-2023 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2023-03-30
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

from odoo import api, fields, models, _


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

##### Overriding standard fields ###

    product_id = fields.Many2one(
        'product.product', 'Product',
        domain=[('type', 'in', ['product', 'consu'])],
        readonly=True,
        required=True,
        states={'confirmed': [('readonly', False)]},
        index=True,
    )

    product_tmpl_id = fields.Many2one(
        'product.template', 'Product Template',
        related='product_id.product_tmpl_id',
        readonly=True,
        index=True,
    )

##### Overriding standard fields ###

    @api.model
    def check_availability(self):
        """
            Re-evaluates ram materials availability on mrp orders
        """
        criteria = [('availability', 'in', ['waiting','partially_available']),
                    ('state', 'in', ['confirmed','planned'])]
        production_ids = self.env['mrp.production'].search(criteria)
        for production_id in production_ids:
            production_id.action_assign()

    @api.model
    def recursive_cancel(self):
        """
            Applies recursive Cancel on mrp orders
        """
        if self:
            criteria = [
                ('origin', '=', self.name),
                ('state', 'in', ['confirmed', 'planned'])
                ]
            for mfg_order_id in self.search(criteria):
                mfg_order_id.recursive_cancel()
            if (self.state in ['confirmed', 'planned']):
                self.action_cancel()

