# -*- encoding: utf-8 -*-
##############################################################################
#
#    Oddo Addons Module, Open Source   
#    Copyright (C) 2024-2025 Codebeex srl (<http://www.codebeex.com>). All Rights Reserved
#
#    Created on: 2025-03-17
#    Author : odoo
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

from copy import deepcopy
from odoo import api, fields, models, _


class MrpProductionSchedule(models.Model):
    _inherit = 'mrp.production.schedule'

    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=False,
        index=True,
    )
    product_category_id = fields.Many2one(
        'product.category',
        related="product_id.product_tmpl_id.categ_id",
        store=True,
        readonly=False,
    )

    @api.model_create_multi
    def create(self, vals_list):
        """ If the BoM is pass at the creation, create MPS for its components """
        existing_mps = []
        new_vals_list =[]
        for i, vals in enumerate(vals_list):
            # Allow to add components of a BoM for MPS already created
            if vals.get('bom_id'):
                mps = self.search([
                    ('product_id', '=', vals['product_id']),
                    ('warehouse_id', '=', vals.get('warehouse_id', self._default_warehouse_id().id)),
                    ('company_id', '=', vals.get('company_id', self.env.company.id)),
                ], limit=1)
                if mps:
                    mps.bom_id = vals.get('bom_id')
                    existing_mps.append((i, mps.id))
            if vals.get('product_category_id'):
                criteria =[
                    ('categ_id', '=', vals['product_category_id']),
                ]
                product_ids = self.env['product.product'].search(criteria)
                for idx, product_id in enumerate(product_ids):
                    newvals = deepcopy(vals)
                    newvals['product_id'] = product_id.id
                    new_vals_list.append(newvals)

        if new_vals_list:
            vals_list = new_vals_list
        for i_remove, __ in reversed(existing_mps):
            del vals_list[i_remove]
                
        mps = super().create(vals_list)

        mps_ids = mps.ids
        for i, mps_id in existing_mps:
            mps_ids.insert(i, mps_id)
        mps = self.browse(mps_ids)

        mps._assign_mps_sequence()

        components_list = set()
        components_vals = []
        for record in mps:
            bom = record.bom_id
            if not bom:
                continue
            dummy, components = bom.explode(record.product_id, 1)
            for component in components:
                if component[0].product_id.is_storable:
                    components_list.add((component[0].product_id.id, record.warehouse_id.id, record.company_id.id))
        for component in components_list:
            if self.env['mrp.production.schedule'].search_count([
                ('product_id', '=', component[0]),
                ('warehouse_id', '=', component[1]),
                ('company_id', '=', component[2]),
            ], limit=1):
                continue
            components_vals.append({
                'product_id': component[0],
                'warehouse_id': component[1],
                'company_id': component[2],
                'is_indirect': True,
                'replenish_trigger': 'never',
            })
        if components_vals:
            self.env['mrp.production.schedule'].create(components_vals)
        return mps
