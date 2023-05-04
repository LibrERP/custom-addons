# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2020-2023 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2023-04-03
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


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    maintenance_id = fields.Many2one(
        'maintenance.request',
        'Maintenance',
        index=True,
    )
    maint_sale_line_id = fields.Many2one(
        'sale.order.line',
        string='Sale Order Line',
        on_delete='set null',
        copy=False,
        index=True,
        ondelete='restrict',
    )
### Overrides standard fields 
    employee_id = fields.Many2one(
        'hr.employee',
        "Technician",
        index=True,
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        readonly=True,
        required=True,
        compute='_compute_new_product',
        )
### Overrides standard fields 

    @api.depends('employee_id')
    def _compute_new_product(self):
        ProdType = self.env['product.product']
        criteria = [
            ('default_code', '=', 'TIME_ENTRY'),
        ]
        for line in self:
            if not line.product_id:
                line.product_id = ProdType.search(criteria, limit=1)

    def _timesheet_mt_preprocess(self, vals):
        """ Deduce other field values from the one given.
            Overrride this to compute on the fly some field that can not be computed fields.
            :param values: dict values for `create`or `write`.
        """
        # project implies analytic account
        if vals.get('maintenance_id') and not vals.get('account_id'):
            maintenance_id = self.env['maintenance.request'].browse(vals.get('maintenance_id'))
            vals['account_id'] = maintenance_id.analytic_account_id.id
            vals['company_id'] = maintenance_id.analytic_account_id.company_id.id
        # employee implies user
        if vals.get('employee_id') and not vals.get('user_id'):
            employee = self.env['hr.employee'].browse(vals['employee_id'])
            vals['user_id'] = employee.user_id.id
        # force customer partner, from the task or the project
        if (vals.get('maintenance_id') and not vals.get('partner_id')):
            partner_id = self.env['maintenance.request'].browse(vals['maintenance_id']).owner_id.id
            if partner_id:
                vals['partner_id'] = partner_id
        return vals

    @api.model
    def create(self, values):
        # compute employee only for timesheet lines, makes no sense for other lines
        if not values.get('employee_id') and values.get('maintenance_id'):
            if values.get('user_id'):
                ts_user_id = values['user_id']
            else:
                ts_user_id = self._default_user()
            values['employee_id'] = self.env['hr.employee'].search([('user_id', '=', ts_user_id)], limit=1).id

        values = self._timesheet_mt_preprocess(values)
        result = super(AccountAnalyticLine, self).create(values)
        return result


