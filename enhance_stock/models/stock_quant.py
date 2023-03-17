# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2020-2023 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2023-03-14
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


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    categ_id = fields.Many2one(
        comodel_name='product.category',
        string='Product Category',
        related='product_id.categ_id',
        index=True,
        store=True,
        )

#### OVERRIDDEN ORIGINAL FIELDS

    product_tmpl_id = fields.Many2one(
        comodel_name='product.template',
        string='Product Template',
        related='product_id.product_tmpl_id',
        index=True,
        readonly=False
        )
    product_uom_id = fields.Many2one(
        comodel_name='uom.uom',
        string='Unit of Measure',
        related='product_id.uom_id',
        index=True,
        readonly=True, 
        )
#### OVERRIDDEN ORIGINAL FIELDS

