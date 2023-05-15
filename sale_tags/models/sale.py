#    Copyright (C) 2020-2023 Didotech srl
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

from datetime import datetime
from datetime import timedelta

from odoo import api, models, fields, _
# from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

import logging
_logger = logging.getLogger(__name__)


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
        total_count = len(self)
        for count, order in enumerate(self, start=1):
            _logger.info(f"Updating Delivery Status: {count} / {total_count} ...")
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
        total_count = len(self)
        for count, order in enumerate(self, start=1):
            _logger.info(f"Updating Payment Status: {count} / {total_count} ...")
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
        total_count = len(self)
        for count, order in enumerate(self, start=1):
            _logger.info(f"Updating Invoice Status: {count} / {total_count} ...")
            ret = 'no'
            if not(order.state in ['cancel']):
                ret = 'to invoice' if order.order_line else 'no'
                invoice_ids = order.order_line.mapped('invoice_lines').mapped('invoice_id').filtered(
                    lambda r: r.type in ['out_invoice', 'out_refund'])
                invoices = len(invoice_ids) if invoice_ids else 0

                if invoices > 0:
                    if invoices == 1:
                        ret = 'invoiced'
                    else:
                        ret = 'invoiced part'
                    invoiced = True
                else:
                    invoiced = False

                for invoice in invoice_ids:
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
        domain = [('state', 'not in', ['cancel'])]
        last_execution = self.get_last_execution()
        if last_execution:
            last_execution += timedelta(minutes=5)
            domain.extend([('write_date', '>=', last_execution.strftime(DEFAULT_SERVER_DATETIME_FORMAT))])
        self.search(domain or []).manage_tags()
        self.set_last_execution()

    @api.model
    def manage_tags(self):
        self._get_invoice_status()
        self._get_delivery_status()
        self._get_payment_status()

    def get_last_execution(self):
        last_execution = self.env["ir.config_parameter"].sudo().get_param("sale.latest_tags_update")
        return last_execution and datetime.strptime(last_execution, DEFAULT_SERVER_DATETIME_FORMAT) or False

    def set_last_execution(self):
        today = fields.datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        self.env["ir.config_parameter"].sudo().set_param("sale.latest_tags_update", today)
