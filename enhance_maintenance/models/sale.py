# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2020-2023 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2023-04-06
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


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    maint_timesheet_ids = fields.One2many(
        'account.analytic.line',
        'maint_sale_line_id',
        'Maintenance Timesheets',
        on_delete='set null',
        index=True,
        copy=False,
        )
    maint_expense_ids = fields.One2many(
        'hr.expense',
        'maint_sale_line_id',
        'Maintenance Expenses',
        on_delete='set null',
        index=True,
        copy=False,
        )
    maintenance_line_ids = fields.One2many(
        'maintenance.spare.line',
        'maint_sale_line_id',
        string='Maintenance Lines',
        on_delete='set null',
        index=True,
        copy=False,
    )

