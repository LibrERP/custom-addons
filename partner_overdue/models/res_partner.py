##############################################################################
#
#    Copyright (C) 2022 Didotech SRL
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
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
import time
from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime, timedelta


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def view_ids(self):
        account_ids = list()

        if self.customer and self.property_account_receivable_id:
            receivable_id = self.property_account_receivable_id
            account_ids.append(receivable_id.id)
            if self.property_account_position_id:
                dest_id = self.property_account_position_id.map_account(receivable_id)
                if dest_id and dest_id.id not in account_ids:
                    account_ids.append(dest_id.id)
        if self.supplier and self.property_account_payable_id:
            payable_id = self.property_account_payable_id
            account_ids.append(payable_id.id)
            if self.property_account_position_id:
                dest_id = self.property_account_position_id.map_account(payable_id)
                if dest_id and dest_id.id not in account_ids:
                    account_ids.append(dest_id.id)
        return account_ids

    def _default_payments(self):
        for partner in self:
            account_ids = partner.view_ids()
            domain = list()
            domain.append(('partner_id', '=', partner.id))
            if account_ids:
                domain.append(('account_id', 'in', account_ids))
            domain.append(('reconciled', '=', False))

            lines = self.env['account.move.line'].search(domain)
            partner.payment_ids = lines

    @api.multi
    def _get_pos_order_invoice_group(self):
        for partner in self:
            invoice_ids = self.env['pos.order.invoice.group'].search([('partner_id', '=', partner.id)], limit=4)
            partner.pos_order_invoice_group_ids = invoice_ids

    def _get_riba_sdd_payment(self):
        due_date = (datetime.now() - timedelta(days=2)).strftime(DEFAULT_SERVER_DATE_FORMAT)
        for partner in self:
            account_view_ids = partner.view_ids()
            partner.payment_riba_ids = self.env['account.move.line.group'].search([
                    ('account_id', 'in', account_view_ids),
                    ('partner_id', '=', partner.id), ('date_maturity_group', '>', due_date)],
                                                                            order='date_maturity_group asc')

    pos_order_invoice_group_ids = fields.One2many(
        compute=_get_pos_order_invoice_group,
        comodel_name='pos.order.invoice.group',
        inverse_name='partner_id',
        string="Fatturato"
    )

    payment_ids = fields.One2many(
        string='Pagamenti aperti',
        comodel_name='account.move.line',
        inverse_name='partner_id',
        compute=_default_payments,
    )

    payment_riba_ids = fields.One2many(
        string='Righe Pagamenti',
        comodel_name='account.move.line.group',
        inverse_name='partner_id',
        compute=_get_riba_sdd_payment,
    )
