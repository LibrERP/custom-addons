# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2020-2021 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2021-07-01
#    Author : Fabio Colognesi
#
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
from odoo.exceptions import UserError

PAYMENT_STATUSES = [
    ('no', "Nothing to pay"),
    ('to pay', "To pay"),
    ('paid part', 'Partially paid'),
    ('paid', "Fully paid"),
    ]

INVOICE_STATUSES = [
    ('no', "Nothing to invoice"),
    ('to invoice', "To invoice"),
    ('invoiced part', 'Partially invoiced'),
    ('invoiced', "Fully invoiced"),
    ]

DELIVERY_STATUSES = [
    ('no', "Nothing to deliver"),
    ('to deliver', "To deliver"),
    ('delivered part', 'Partially delivered'),
    ('delivered', "Fully delivered"),
    ]


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def _get_delivery_status(self):
        for order in self:
            ret = 'no'
            if not(order.state in ['cancel']):
                ret = 'to deliver' if order.order_line else 'no'
                deliveries = len(order.picking_ids) if order.picking_ids else 0
                ret = 'to deliver' if (deliveries > 0) else ret
                ret = 'delivered part' if (deliveries > 1) else ret
                delivered = True if (deliveries > 0) else False
                for picking in order.picking_ids:
                    delivered &= (picking.state in ['done', 'cancel'])
                ret = 'delivered' if (deliveries and delivered) else ret
            order.deliveries_status = ret

    @api.multi
    def _get_payment_status(self):
        for order in self:
            ret = 'no'
            if not(order.state in ['cancel']):
                ret = 'to pay' if order.order_line else 'no'
                invoices = len(order.invoice_ids) if order.invoice_ids else 0
                ret = 'to pay' if (invoices > 0) else ret
                part_paid = True if 'paid' in order.invoice_ids.mapped('state') else False
                ret = 'paid part' if (part_paid and invoices > 1) else ret
                paid = True if (invoices > 0) else False
                for invoice in order.invoice_ids:
                    paid &= (invoice.state in ['cancel', 'paid'])
                ret = 'paid' if paid else ret
            order.payments_status = ret

    @api.multi
    def _get_invoice_status(self):
        for order in self:
            ret = 'no'
            if not(order.state in ['cancel']):
                ret = 'to invoice' if order.order_line else 'no'
                invoices = len(order.invoice_ids) if order.invoice_ids else 0
                ret = 'invoiced' if (invoices > 0) else ret
                ret = 'invoiced part' if (invoices > 1) else ret
                invoiced = True if (invoices > 0) else False
                for invoice in order.invoice_ids:
                    invoiced &= (invoice.state in ['open', 'cancel', 'paid'])
                ret = 'invoiced' if invoiced else ret
            order.invoices_status = ret

    invoices_status = fields.Selection(
        INVOICE_STATUSES,
        string='Invoice Status',
        compute='_get_invoice_status',
        store=True, readonly=True, copy=False)

    deliveries_status = fields.Selection(
        DELIVERY_STATUSES,
        string='Delivery Status',
        compute='_get_delivery_status',
        store=True, readonly=True, copy=False)

    payments_status = fields.Selection(
        PAYMENT_STATUSES,
        string='Payment Status',
        compute='_get_payment_status',
        store=True, readonly=True, copy=False)

    @api.model
    def check_tag_on_sale_orders(self):
        domain = [('state', 'in', ['draft', 'sent', 'sale', 'done'])]
        self.search(domain or []).manage_tags()

    @api.model
    def manage_tags(self):
        self._get_invoice_status()
        self._get_delivery_status()
        self._get_payment_status()

