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
from odoo.addons import decimal_precision as dp
from odoo import exceptions, _

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    owner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        index=True,
        domain="[('customer', '=', 1)]",
    )

    sales_date = fields.Date('Sales Date')


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    owner_id = fields.Many2one(
        'res.partner',
        related='equipment_id.owner_id',
        string='Customer',
        store=True,
        readonly=True,
        index=True,
    )

    serial_no = fields.Char(
        related='equipment_id.serial_no',
        string='Serial Number / Plate',
        store=True,
        readonly=True,
        index=True,
    )

    spare_ids = fields.One2many(
        'maintenance.spare.line',
        'maintenance_id',
        string='Spare Parts',
        index=True,
        copy=True,
        auto_join=True
    )
    spare_price = fields.Float(
        "Total Price",
        compute='_compute_spare_price',
        store=True,
        readonly=True,
        help="Total Spare Parts Price.",
    )
    timesheet_ids = fields.One2many(
        'account.analytic.line',
        'maintenance_id',
        'Timesheets',
        index=True,
        copy=False,
        )
    remaining_hours = fields.Float(
        "Remaining Hours",
        compute='_compute_remaining_hours',
        store=True,
        readonly=True,
        help="Total remaining time [hours].",
    )
    effective_hours = fields.Float(
        "Hours Spent",
        compute='_compute_effective_hours',
        compute_sudo=True,
        store=True,
        help="Computed using the sum of the maintenance work done.",
    )
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string="Analytic Account",
        copy=False,
        ondelete='set null',
        index=True,
        help="Links this maintenance to an analytic account.",
    )
    editable = fields.Boolean(
        compute='_compute_editable',
        default=True
    )
    expense_ids = fields.One2many(
        'hr.expense',
        'maintenance_id',
        'Expenses',
        index=True,
        copy=False,
        )
    effective_expenses = fields.Float(
        "Effective Expenses",
        compute='_compute_effective_expenses',
        compute_sudo=True,
        store=True,
        help="Computed using the sum of all maintenance expenses done.",
    )
    refused_expenses = fields.Float(
        "Refused Expenses",
        compute='_compute_refused_expenses',
        compute_sudo=True,
        store=True,
        help="Computed using the sum of the maintenance refused expenses.",
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.user.company_id.currency_id,
    )
    invoice_count = fields.Integer(
        string='Invoice Count',
        compute='_get_invoiced',
        readonly=True,
        copy=False,
    )
    invoice_ids = fields.Many2many(
        "account.invoice",
        string='Invoices',
        compute='_get_invoiced',
        readonly=True,
        copy=False,
    )
    sales_count = fields.Integer(
        string='Invoice Count',
        compute='_get_sold',
        readonly=True,
        copy=False,
    )
    sale_ids = fields.Many2many(
        "sale.order",
        string='Sale Orders',
        compute='_get_sold',
        readonly=True,
        copy=False,
    )
    away_ids = fields.One2many(
        'maintenance.away.line',
        'maintenance_id',
        string='Away Costs',
        index=True,
        copy=False,
        auto_join=True
    )
    away_price = fields.Float(
        "Total Costs",
        compute='_compute_away_price',
        store=True,
        readonly=True,
        help="Total Aways Costs.",
    )

    @api.depends('invoice_count')
    def _get_invoiced(self):
        lineType = self.env['maintenance.sale.rel']
        for maintenance_id in self:
            criteria = [
                ('maintenance_id', '=', maintenance_id.id),
            ]
            line_ids = lineType.search(criteria)
            if line_ids:
                sale_ids = line_ids.mapped('sale_id')
                if sale_ids:
                    invoice_ids = sale_ids.mapped('invoice_ids')
                    if invoice_ids:
                        counted = len(invoice_ids)
                        maintenance_id.update({
                            'invoice_count': counted,
                            'invoice_ids': [(6, 0, invoice_ids.ids)]
                        })

    @api.depends('sales_count')
    def _get_sold(self):
        lineType = self.env['maintenance.sale.rel']
        for maintenance_id in self:
            criteria = [
                ('maintenance_id', '=', maintenance_id.id),
            ]
            line_ids = lineType.search(criteria)
            if line_ids:
                sale_ids = line_ids.mapped('sale_id')
                if sale_ids:
                    counted = len(sale_ids)
                    maintenance_id.update({
                        'sales_count': counted,
                        'sale_ids': [(6, 0, sale_ids.ids)]
                    })

    @api.depends('spare_ids.product_price')
    def _compute_spare_price(self):
        for maintenance in self:
            maintenance.spare_price = round(sum(maintenance.spare_ids.mapped('product_price')), 2)

    @api.depends('away_ids.product_price')
    def _compute_away_price(self):
        for maintenance in self:
            maintenance.away_price = round(sum(maintenance.away_ids.mapped('product_price')), 2)

    @api.depends('timesheet_ids.unit_amount')
    def _compute_effective_hours(self):
        for maintenance in self:
            maintenance.effective_hours = round(sum(maintenance.timesheet_ids.mapped('unit_amount')), 2)
            if maintenance.stage_id:
                stegeType = self.env['maintenance.stage']
                stage_id = stegeType.browse(maintenance.stage_id.id)
                if stage_id.sequence == 1:
                    criteria = [('sequence', '=', 2)]
                    stage_id = stegeType.search(criteria, limit=1)
                    maintenance.stage_id = stage_id.id

    @api.depends('effective_hours', 'duration')
    def _compute_remaining_hours(self):
        for maintenance in self:
            maintenance.remaining_hours = maintenance.duration - maintenance.effective_hours

    @api.depends('stage_id')
    def _compute_editable(self):
        for maintenance in self:
            if maintenance.stage_id:
                stegeType = self.env['maintenance.stage']
                stage_id = stegeType.browse(maintenance.stage_id.id)
                if (stage_id.sequence in [1,2]):
                    maintenance.editable = True
                else:
                    maintenance.editable = False

    @api.depends('expense_ids.unit_amount_line')
    def _compute_effective_expenses(self):
        for maintenance in self:
            maintenance.effective_expenses = round(sum(maintenance.expense_ids.mapped('unit_amount_line')), 2)
            for expense_id in maintenance.expense_ids:
                expense_id.unit_amount = expense_id.unit_amount_line
                if expense_id.maint_sale_line_id:
                    expense_id.state = 'approved'
                if not expense_id.is_acceptable:
                    expense_id.is_refused = True
                    expense_id.state = 'refused'

    @api.depends('effective_expenses')
    def _compute_refused_expenses(self):
        for maintenance in self:
            maintenance.refused_expenses = 0
            for expense_id in maintenance.expense_ids:
                expense_id.unit_amount = expense_id.unit_amount_line
                if not expense_id.is_acceptable:
                    maintenance.refused_expenses += expense_id.unit_amount_line

    @api.onchange('expense_ids.name')
    def _onchange_expense_name(self):
        for expense_id in self.expense_ids:
            if expense_id.maint_sale_line_id:
                expense_id.state = 'reported'
            if not expense_id.is_acceptable:
                expense_id.is_refused = True
                expense_id.state = 'refused'
            if expense_id.name and expense_id.unit_amount:
                criteria = [('default_code', '=', 'EXP_GEN')]
                product_id = self.env['product.product'].search(criteria, limit=1)
                if product_id:
                    expense_id.product_id = product_id.id

    @api.model
    def create(self, values):
        """
            Creates an analytic account if maintenance doesn't provide one
        """
        if not values.get('analytic_account_id'):
            analytic_account = self.env['account.analytic.account'].create({
                'name': values.get('name', _('Maintenance Analytic Account')),
                'company_id': values.get('company_id', self.env.user.company_id.id),
                'partner_id': values.get('partner_id'),
                'active': True,
            })
            values['analytic_account_id'] = analytic_account.id
        return super(MaintenanceRequest, self).create(values)

    def open_view_invoice(self):
        """
            Creates an analytic account if maintenance doesn't provide one
        """
        return {
            'name': _('Invoices Related'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            "view_type": "form",
            'res_model': 'account.invoice',
            'context': self.env.context,
            'domain': [('id', 'in', self.mapped('invoice_ids').ids)],
        }

    def open_view_sale(self):
        """
            Creates an analytic account if maintenance doesn't provide one
        """
        return {
            'name': _('Sale Orders Related'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            "view_type": "form",
            'res_model': 'sale.order',
            'context': self.env.context,
            'domain': [('id', 'in', self.mapped('sale_ids').ids)],
        }

    @api.model
    def action_create_sale_orders(self):
        orderType = self.env['sale.order']
        show_timesheet_name = self.env['ir.config_parameter'].sudo().get_param('enhance_maintenance.show_timesheet_name')
        show_expense_name = self.env['ir.config_parameter'].sudo().get_param('enhance_maintenance.show_expense_name')
        show_away_name = self.env['ir.config_parameter'].sudo().get_param('enhance_maintenance.show_away_name')

        for maintenance_id in self:
            if not(maintenance_id.owner_id):
                raise exceptions.Warning(_("Customer is not set."))
            sale_order_id = orderType
            if maintenance_id.mapped('sale_ids'):
                for order_id in maintenance_id.mapped('sale_ids'):
                    if order_id.state in ['draft','sent']:
                        sale_order_id = order_id
                        break
            if not sale_order_id and maintenance_id.owner_id:
                values = {
                    'pricelist_id': maintenance_id.owner_id.property_product_pricelist and maintenance_id.owner_id.property_product_pricelist.id or False,
                    'payment_term_id': maintenance_id.owner_id.property_payment_term_id and maintenance_id.owner_id.property_payment_term_id.id or False,
                    'partner_id': maintenance_id.owner_id.id,
                    'partner_invoice_id': maintenance_id.owner_id.id,
                    'partner_shipping_id': maintenance_id.owner_id.id,
                    'user_id': maintenance_id.owner_id.user_id.id or maintenance_id.owner_id.commercial_partner_id.user_id.id or self.env.uid
                }
                sale_order_id = orderType.create(values)
            if sale_order_id:
                self.check_rel(sale_order_id, maintenance_id)
                partner_shipping_id = sale_order_id.partner_shipping_id
                for spare_id in maintenance_id.spare_ids:
                    if not spare_id.maint_sale_line_id:
                        product_id = spare_id.product_id
                        price = spare_id.product_price
                        product_uom_qty = spare_id.product_uom_qty
                        product_name = product_id.name
                        sale_line_id = self.create_sale_order_line(price, product_id, product_name, product_uom_qty, sale_order_id, maintenance_id, partner_shipping_id)
                        if sale_line_id:
                            spare_id.maint_sale_line_id = sale_line_id.id
                for timesheet_id in maintenance_id.timesheet_ids:
                    if not timesheet_id.maint_sale_line_id:
                        employee_id = timesheet_id.employee_id
                        product_id = timesheet_id.product_id
                        price = employee_id.timesheet_cost
                        product_uom_qty = timesheet_id.unit_amount
                        delivered_qty = product_uom_qty
                        product_name = timesheet_id.name if show_timesheet_name else product_id.name
                        sale_line_id = self.create_sale_order_line(price, product_id, product_name, product_uom_qty, sale_order_id, maintenance_id, partner_shipping_id)
                        if sale_line_id:
                            sale_line_id.write({'qty_delivered': delivered_qty})
                            timesheet_id.maint_sale_line_id = sale_line_id.id
                for expense_id in maintenance_id.expense_ids:
                    if not expense_id.maint_sale_line_id:
                        if expense_id.is_acceptable:
                            product_id = expense_id.product_id
                            price = expense_id.unit_amount_line
                            product_name = expense_id.name if show_expense_name else product_id.name
                            sale_line_id = self.create_sale_order_line(price, product_id, product_name, 1, sale_order_id, maintenance_id, partner_shipping_id)
                            if sale_line_id:
                                sale_line_id.write({'qty_delivered': 1})
                                expense_id.maint_sale_line_id = sale_line_id.id
                for away_id in maintenance_id.away_ids:
                    if not away_id.maint_sale_line_id:
                        product_id = away_id.product_id
                        price = away_id.product_price
                        product_uom_qty = away_id.product_uom_qty
                        product_name = away_id.name if show_away_name else product_id.name
                        sale_line_id = self.create_sale_order_line(price, product_id, product_name, product_uom_qty, sale_order_id, maintenance_id, partner_shipping_id)
                        if sale_line_id:
                            away_id.maint_sale_line_id = sale_line_id.id

    @api.model
    def check_rel(self, sale_order_id, maintenance_id):
        lineType = self.env['maintenance.sale.rel']
        criteria = [
            ('sale_id', '=', sale_order_id.id),
            ('maintenance_id', '=', maintenance_id.id),
        ]
        if not lineType.search(criteria, limit=1):
            lineType.create({
                'sale_id': sale_order_id.id,
                'maintenance_id': maintenance_id.id,
            })


    @api.model
    def create_sale_order_line(self, price, product_id, product_name, product_uom_qty, sale_order_id, maintenance_id, partner_id):
        lineType = self.env['sale.order.line']
        tax_id = product_id.taxes_id[0] if product_id.taxes_id else self.env.user.company_id.account_sale_tax_id
        taxes = tax_id.compute_all(price, sale_order_id.currency_id, product_uom_qty, product=product_id, partner=partner_id)
        values = {
            'name': product_name,
            'product_id': product_id.id,
            'product_uom': product_id.uom_id.id,
            'product_uom_qty': product_uom_qty,
            'order_id': sale_order_id.id,
            'price_unit': price,
            'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
            'price_total': taxes['total_included'],
            'price_subtotal': taxes['total_excluded'],
            'maintenance_id': maintenance_id.id,
        }
        return lineType.create(values)
 

class MaintenanceSpareLine(models.Model):
    _name = 'maintenance.spare.line'
    _description = 'Spare Product Line'
    _order = 'maintenance_id, sequence, product_id'

    maintenance_id = fields.Many2one(
        'maintenance.request',
        string='Maintenance Request',
        required=True,
        ondelete='cascade',
        index=True,
        copy=False,
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        domain=[('sale_ok', '=', True)],
        change_default=True,
        index=True,
        ondelete='restrict',
    )
    product_uom_qty = fields.Float(
        string='Ordered Quantity',
        digits=dp.get_precision('Product Unit of Measure'),
        required=True,
        default=1.0,
    )
    product_uom = fields.Many2one(
        'uom.uom',
        related='product_id.uom_id',
        string='Unit of Measure',
        index=True,
    )
    product_note = fields.Text(
        related='product_id.description',
        string='Product Note',
        readonly=True,
    )
    product_price = fields.Float(
        related='product_id.lst_price',
        string='Product Price',
        digits=dp.get_precision('Product Price'),
        store=True,
        readonly=True,
    )
    sequence = fields.Integer(string='Sequence', default=10)
    maint_sale_line_id = fields.Many2one(
        'sale.order.line',
        string='Sale Order Line',
        on_delete='set null',
        copy=False,
        index=True,
    )


class MaintenanceSaleRel(models.Model):
    _name = 'maintenance.sale.rel'
    _description = "Maintenance Sale Order Relations"

    sale_id = fields.Many2one(
        'sale.order',
        string='Sale Order',
        index=True,
        ondelete='cascade',
    )
    maintenance_id = fields.Many2one(
        'maintenance.request',
        string='Maintenance',
        index=True,
        ondelete='cascade',
    )


class MaintenanceInvoiceRel(models.Model):
    _name = 'maintenance.invoice.rel'
    _description = "Maintenance Invoice Relations"

    invoice_id = fields.Many2one(
        'account.invoice',
        string='Invoice',
        index=True,
        ondelete='cascade',
    )
    maintenance_id = fields.Many2one(
        'maintenance.request',
        string='Maintenance',
        index=True,
        ondelete='cascade',
    )


class MaintenanceAwayLine(models.Model):
    _name = 'maintenance.away.line'
    _description = 'Away Line'
    _order = 'maintenance_id, sequence, product_id'

    maintenance_id = fields.Many2one(
        'maintenance.request',
        string='Maintenance Request',
        required=True,
        ondelete='cascade',
        index=True,
        copy=False,
    )
    name = fields.Text(
        string='Name',
        help='Usable in Sale Order & Invoice lines.'
    )
    date = fields.Date(
        string="Date",
        required=True,
        default=fields.Date.context_today,
        )
    product_id = fields.Many2one(
        'product.product',
        string='Away',
        required=True,
        ondelete='restrict',
        index=True,
        compute='_compute_product',
        )
    product_uom_qty = fields.Float(
        string='Quantity',
        digits=dp.get_precision('Product Unit of Measure'),
        required=True,
        default=1.0,
    )
    product_uom = fields.Many2one(
        'uom.uom',
        related='product_id.uom_id',
        string='Unit of Measure',
        index=True,
    )
    product_note = fields.Text(
        string='Note',
        help='Usable for internal knowledge.'
    )
    product_unit_price = fields.Float(
        related='product_id.lst_price',
        string='Unit Cost',
        digits=dp.get_precision('Product Price'),
        store=True,
        readonly=True,
    )
    product_price = fields.Float(
        string='Cost',
        digits=dp.get_precision('Product Price'),
        store=True,
        readonly=True,
        compute='_compute_price',
    )
    sequence = fields.Integer(string='Sequence', default=10)
    maint_sale_line_id = fields.Many2one(
        'sale.order.line',
        string='Sale Order Line',
        on_delete='set null',
        copy=False,
        index=True,
    )

    @api.model
    def _compute_product(self):
        ret = self.env['product.product']
        criteria = [('default_code', '=', 'AWAY_ENTRY')]
        product_id = self.env['product.product'].search(criteria, limit=1)
        if product_id:
            for away in self:
                away.product_id = product_id.id
 
    @api.depends('product_uom_qty','product_unit_price')
    def _compute_price(self):
        for line in self:
            if line.product_uom_qty and line.product_unit_price:
                line.product_price = line.product_uom_qty * line.product_unit_price

