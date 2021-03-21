# -*- coding: utf-8 -*-
# Copyright 2020 Andrei Levin - Didotech srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api
import datetime
from dateutil.relativedelta import relativedelta


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def _get_document_type_and_date(self):
        delivery_document_model = self.env['stock.picking.package.preparation']

        if self.env.context.get('active_model') == 'sale.order':
            order = self.env['sale.order'].browse(self.env.context['active_id'])
            delivery_documents = order.ddt_ids
            delivery_document = delivery_documents and delivery_documents[0] or False
        else:
            # Take the last transport document
            delivery_document = delivery_document_model.search([
                ('id', 'in', self.env.context['active_ids'])
            ], order='date desc', limit=1)[0]

        if delivery_document and delivery_document.date.month == datetime.datetime.now().month:
            domain = [('code', '=', 'TD24')]
            document_date = datetime.datetime.now()
        elif delivery_document and delivery_document.date.month == (datetime.datetime.now() - relativedelta(months=1)).month \
                and datetime.datetime.now().day < 11:
            # TD is from previous month but we are in the first 10 days of the next month
            domain = [('code', '=', 'TD24')]
            # Invoice date is the last day from the previous month
            today = datetime.datetime.now()
            document_date = datetime.datetime(year=today.year, month=today.month, day=1) - relativedelta(days=1)
        elif delivery_document:
            domain = [('code', '=', 'TD25')]
            document_date = datetime.datetime.now()
        else:
            domain = [('code', '=', 'TD01')]
            document_date = datetime.datetime.now()

        return {
            'domain': domain,
            'document_date': document_date.date()
        }

    def _get_document_fiscal_type(self, type=None, partner=None,
                                  fiscal_position=None, journal=None):

        if self.env.context.get('active_model') in ('stock.picking.package.preparation', 'sale.order', 'ddt.invoicing')\
                and type == 'out_invoice' or not type:

            for invoice_line in self.invoice_line_ids:
                is_downpayment = [sale_line for sale_line in invoice_line.sale_line_ids if sale_line.is_downpayment]
                if is_downpayment:
                    break
            else:
                is_downpayment = False

            if is_downpayment:
                dt = self.env['fiscal.document.type'].search([('code', '=', 'TD02')]).ids
            else:
                document_data = self._get_document_type_and_date()
                dt = self.env['fiscal.document.type'].search(document_data['domain']).ids
        else:
            dt = super()._get_document_fiscal_type(
                type=type, partner=partner, fiscal_position=fiscal_position, journal=journal
            )

        return dt

    @api.model
    def create(self, values):
        if self.env.context.get('active_model') in ('stock.picking.package.preparation', 'sale.order', 'ddt.invoicing')\
                and values.get('type', 'out_invoice') == 'out_invoice':
            document_data = self._get_document_type_and_date()
            values['date_invoice'] = document_data['document_date']
        return super().create(values)
