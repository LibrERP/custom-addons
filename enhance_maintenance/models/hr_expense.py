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

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class Expense(models.Model):
    _inherit = "hr.expense"

    maintenance_id = fields.Many2one(
        'maintenance.request',
        'Maintenance',
        copy=False,
        index=True,
    )
    maint_sale_line_id = fields.Many2one(
        'sale.order.line',
        string='Sale Order Line',
        on_delete='set null',
        copy=False,
        index=True,
    )
    unit_amount_line = fields.Float(
        "Unit Price",
        readonly=True,
        required=True,
        states={
            'draft': [('readonly', False)],
            },
        digits=dp.get_precision('Product Price'),
        )

### Overrides standard fields 
    state = fields.Selection(
        [
            ('draft', 'To Submit'),
            ('reported', 'Submitted'),
            ('approved', 'Approved'),
            ('done', 'Paid'),
            ('refused', 'Refused'),
        ], 
        compute='_compute_state',
        string='Status',
        copy=False,
        index=True,
        readonly=True,
        store=True,
        default='draft',
        help="Status of the expense.",
        )
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        readonly=True,
        states={'draft': [('readonly', False)],
                'reported': [('readonly', False)],
                'refused': [('readonly', False)]},
        domain=[('can_be_expensed', '=', True)],
        required=True,
        compute='_compute_product',
        )
### Overrides standard fields 

    is_acceptable = fields.Boolean(
        "Expense accepted by manager",
        default=True,
        copy=False,
        )

    @api.model
    def _compute_product(self):
        ret = self.env['product.product']
        criteria = [('default_code', '=', 'EXP_GEN')]
        product_id = self.env['product.product'].search(criteria, limit=1)
        if product_id:
            for expense_id in self:
                expense_id.product_id = product_id.id
 
