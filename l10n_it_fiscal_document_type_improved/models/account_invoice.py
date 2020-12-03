# -*- coding: utf-8 -*-
# Copyright 2020 Andrei Levin - Didotech srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api
import datetime


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def _get_document_fiscal_type(self, type=None, partner=None,
                                  fiscal_position=None, journal=None):

        delivery_document_model = self.env['stock.picking.package.preparation']
        if self.env.context['active_model'] == 'stock.picking.package.preparation' \
                and type == 'out_invoice' or not type:

            delivery_document = delivery_document_model.browse(self.env.context['active_id'])
            if delivery_document.date.month == datetime.datetime.now().month:
                domain = [('code', '=', 'TD24')]
            else:
                domain = [('code', '=', 'TD25')]
            dt = self.env['fiscal.document.type'].search(domain).ids
        else:
            dt = super()._get_document_fiscal_type(
                type=type, partner=partner, fiscal_position=fiscal_position, journal=journal
            )

        return dt
