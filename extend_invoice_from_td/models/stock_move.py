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
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools import float_is_zero

import odoo.addons.decimal_precision as dp

from odoo.fields import first
from odoo.tools.misc import formatLang, format_date


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def invoice_line_create(self, invoice_id, qty):
        """
        :param invoice_id: integer
        :param qty: float quantity to invoice
        """
        precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        for line in self:
            if not float_is_zero(qty, precision_digits=precision):
                vals = line._prepare_invoice_line(qty=qty, invoice_id=invoice_id)
                self.env['account.invoice.line'].with_context(
                    skip_update_line_ids=True).create(vals)
        invoice_id.compute_taxes()

    @api.multi
    def _prepare_invoice_line(self, qty, invoice_id):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        """
        self.ensure_one()
        product = self.product_id.with_context(force_company=self.company_id.id)
        account = product.property_account_income_id or product.categ_id.property_account_income_categ_id

        if not account and self.product_id:
            raise UserError(
                'Please define income account for this product: {prod} (id:{id}) - or for its category: {cat}.'.format(
                    prod=self.product_id.name,
                    id=self.product_id.id,
                    cat=self.product_id.categ_id.name
                ))
        rslt = product.partner_ref
        if product.description_sale:
            rslt += '\n' + product.description_sale

        price_unit = product.lst_price or 0.0
        tax_ids = product.taxes_id

        if self.sale_line_id:
            res = self.sale_line_id._prepare_invoice_line(qty)
            res.update({
                'name': rslt,
                'price_unit': self.sale_line_id.price_unit,
                'discount': self.sale_line_id.discount,
                'origin': self.picking_id.name,
                'invoice_id': invoice_id.id,
                'invoice_line_tax_ids': [(6, 0, [self.sale_line_id.tax_id.id])],
            })
        else:
            if invoice_id.partner_id.discount_class_id:
                discount = invoice_id.partner_id.discount_class_id.percent
                discount_on_price = discount * price_unit / 100
                # price_unit = price_unit - discount_on_price
                price_unit = price_unit
            else:
                discount = False

            taxes = False
            if tax_ids:
                taxes = tax_ids.compute_all(
                    price_unit,
                    invoice_id.currency_id,
                    qty,
                    product=product,
                    partner=invoice_id.partner_id)

            if tax_ids and tax_ids.ids:
                taxes_ids = [(6, 0, tax_ids.ids)]
            else:
                taxes_ids = False

            res = {
                'name': rslt,
                'price_unit': price_unit,
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
                'quantity': qty,
                'invoice_id': invoice_id.id,
                'partner_id': invoice_id.partner_id.id,
                'origin': self.picking_id.name,
                'account_id': account.id,
                'uom_id': product.uom_id.id,
                'product_id': product.id or False,
                'invoice_line_tax_ids': taxes_ids,
            }
            if discount:
                res.update({'discount': discount})

        return res
