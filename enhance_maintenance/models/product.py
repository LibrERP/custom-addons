# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2020-2023 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2023-03-24
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


class Product(models.Model):
    _inherit = 'product.product'

    maintenance_id = fields.Many2one(
        'maintenance.spare.line',
        string='Spare Product Line',
        index=True,
    )
