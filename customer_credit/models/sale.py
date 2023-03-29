##############################################################################
#
#    Copyright (C) 2022-2023 Didotech srl
#    (<http://www.didotech.com/>).
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


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('amount_total')
    def _compute_limit(self):
        for order in self:
            order.order_credit_limit = 0.0
            order.order_advance_remaining = 0.0
            order.sale_warn = False
            # ha un fido
            if order.partner_id.credit_limit:
                order.order_credit_limit = order.partner_id.fido_residuo
                if order.state == 'draft':
                     order.order_credit_limit -= order.amount_total

                if order.order_credit_limit < 0:
                    order.sale_warn = True
                    # res = {}

            if order.partner_id:
                amount = 0
                fiscal_doc_type = self.env['fiscal.document.type'].search_read([('code', '=', 'TD02')], ('id', 'code'))
                if fiscal_doc_type:
                    invoices = order.invoice_ids.filtered(
                        lambda i: i.state == 'paid' and i.fiscal_document_type_id.id == fiscal_doc_type[0]['id'])
                    if invoices:
                        for invoice in invoices:
                            amount += invoice.amount_total
                        order.order_advance_remaining = order.amount_total - amount

    order_credit_limit = fields.Float(
        string='Fido residuo',
        compute=_compute_limit,
    )

    order_advance_remaining = fields.Float(
        string='Residuo Acconto',
        compute=_compute_limit,
    )

    sale_warn = fields.Boolean(
        string='Avviso',
        compute=_compute_limit,
    )

    credit_warn = fields.Char(
        string="Avviso fido",
        default="Attenzione: Il fido è stato superato",
    )

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super().onchange_partner_id()
        self._compute_limit()
        # self.order_credit_limit = self.partner_id.fido_residuo - self.amount_total
