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
        # Take the last transport document
        delivery_document = delivery_document_model.search([
            ('id', 'in', self.env.context['active_ids'])
        ], order='date desc', limit=1)[0]

        if delivery_document.date.month == datetime.datetime.now().month:
            domain = [('code', '=', 'TD24')]
            document_date = datetime.datetime.now()
        elif delivery_document.date.month == (datetime.datetime.now() - relativedelta(months=1)).month \
                and datetime.datetime.now().day < 11:
            # TD is from previous month but we are in the first 10 days of the next month
            domain = [('code', '=', 'TD24')]
            # Invoice date is the last day from the previous month
            today = datetime.datetime.now()
            document_date = datetime.datetime(year=today.year, month=today.month, day=1) - relativedelta(days=1)
        else:
            domain = [('code', '=', 'TD25')]
            document_date = datetime.datetime.now()

        return {
            'domain': domain,
            'document_date': document_date.date()
        }

    def _get_document_fiscal_type(self, type=None, partner=None,
                                  fiscal_position=None, journal=None):

        if self.env.context['active_model'] == 'stock.picking.package.preparation' \
                and type == 'out_invoice' or not type:

            document_data = self._get_document_type_and_date()
            dt = self.env['fiscal.document.type'].search(document_data['domain']).ids
        else:
            dt = super()._get_document_fiscal_type(
                type=type, partner=partner, fiscal_position=fiscal_position, journal=journal
            )

        return dt

    def create(self, values):
        if self.env.context['active_model'] == 'stock.picking.package.preparation' \
                and values.get('type', 'out_invoice') == 'out_invoice':
            document_data = self._get_document_type_and_date()
            values['date_invoice'] = document_data['document_date']
        return super().create(values)
