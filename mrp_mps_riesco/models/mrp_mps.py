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

from datetime import datetime
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
    sales_orders = fields.Boolean('Use Sale Quotations to identify products.')
    start_date = fields.Date('Start Date')
    final_date = fields.Date('End Date')

    def get_by_sales(self, vals):
        """
            Composes MPS and their forecasted quantities, based on products
             listed inside sales orders in quotation status. 
        """
        mps_ids = self.env['mrp.production.schedule']
        forecastType = self.env['mrp.product.forecast']
        product_ids = self.env['product.product']
        start_date = vals.get('start_date', datetime.now().date().strftime("%Y-%m-%d"))
        final_date = vals.get('final_date', datetime.now().date().strftime("%Y-%m-%d"))
        criteria =[
            ('state', 'in', ['draft','sent']),
            ('commitment_date', '>=', start_date),
            ('commitment_date', '<=', final_date),
        ]
        sale_ids = self.env['sale.order'].search(criteria)
        for sale_line_id in sale_ids.mapped('order_line'):
            product_id = sale_line_id.product_id
            qty_line = sale_line_id.product_uom_qty
            commitment_date = sale_line_id.order_id.commitment_date.date().strftime("%Y-%m-%d")
            criteria =[
                ('product_id', '=', product_id.id),
                ('warehouse_id', '=', vals.get('warehouse_id', self._default_warehouse_id().id)),
                ('company_id', '=', vals.get('company_id', self.env.company.id)),
            ]
            mps_id = self.search(criteria, limit=1)
            if not mps_id:
                product_ids += product_id
                newvals = deepcopy(vals)
                newvals['product_id'] = product_id.id
                newvals['product_category_id'] = product_id.categ_id.id
                mps_id = super().create([newvals])
                if mps_id:
                    values = {
                        'forecast_qty': qty_line,
                        'date': commitment_date,
                        'production_schedule_id': mps_id.id,
                    }
                    forecast_id = forecastType.create([values])
            else:
                if mps_id.forecast_ids:
                    forecast_id = mps_id.forecast_ids.filtered_domain([('date', '=', commitment_date)])
                    if forecast_id:
                        forecast_qty = forecast_id.forecast_qty + qty_line
                        forecast_id.write({"forecast_qty": forecast_qty})
                    else:
                        values = {
                            'forecast_qty': qty_line,
                            'date': commitment_date,
                            'production_schedule_id': mps_id.id,
                        }
                        forecast_id = forecastType.create([values])
            if mps_id:
                mps_ids += mps_id
        return mps_ids

    @api.model_create_multi
    def create(self, vals_list):
        """ If the BoM is pass at the creation, create MPS for its components """
        existing_mps = []
        new_vals_list =[]
        go_ahead = False
        sales_mps = mps = self.env['mrp.production.schedule']
        for i, vals in enumerate(vals_list):
            if vals.get('product_id'):
                go_ahead = True
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
            # Compose search using product categories amd forecasted quantity
            if vals.get('product_category_id'):
                criteria =[
                    ('categ_id', '=', vals['product_category_id']),
                    ('virtual_available', '>', 0),
                ]
                product_ids = self.env['product.product'].search(criteria)
                if product_ids:
                    go_ahead = True
                for idx, product_id in enumerate(product_ids):
                    newvals = deepcopy(vals)
                    newvals['product_id'] = product_id.id
                    new_vals_list.append(newvals)
            # Compose search using sales quotations and their dates
            if vals.get('sales_orders'):
                sales_mps += self.get_by_sales(vals)
        if sales_mps:
            go_ahead = True

        if new_vals_list:
            vals_list = new_vals_list
            
        for i_remove, __ in reversed(existing_mps):
            del vals_list[i_remove]
                
        if go_ahead:
            if sales_mps:
                mps = sales_mps
                vals_list = []
            else:
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
