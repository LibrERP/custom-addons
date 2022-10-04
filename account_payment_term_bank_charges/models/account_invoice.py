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


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.onchange('payment_term_id')
    def _onchange_payment_term_id_extended(self):
        # res = super()._onchange_payment_term_id()
        payment_term_model = self.env['account.payment.term']
        invoice_line_ids = []
        # payment_term_charges_ids = self._payment_term_charges_ids()
        spese_incasso = payment_term_model.browse(self.payment_term_id.id)
        product_charges_ids = self._product_charges_ids()
        if self.invoice_line_ids and self.payment_term_id:
            new_invoice_line = []
            for line in self.invoice_line_ids:
                if line.id in product_charges_ids:
                    line.unlink()
                else:
                    new_invoice_line.append(line)

            # if spese_incasso and spese_incasso.spese_incasso_id:
            #     vals = self._spese_incasso_vals(spese_incasso.spese_incasso_id)
            #     new_invoice_line.append([0, 0, vals])

            self.invoice_line_ids = new_invoice_line

    def _payment_term_charges_ids(self):
        records = self.env['account.payment.term'].search([('spese_incasso_id', '!=', False)])
        return [record.id for record in records]

    def _product_charges_ids(self):
        records = self.env['account.payment.term'].search([('spese_incasso_id', '!=', False)])
        products = [item.spese_incasso_id for item in records]
        return [product.id for product in products]

    def _spese_incasso_vals(self, product):
        account_invoice_line_vals = {
            'invoice_id': self.id,
            'product_id': product.id,
            'name': product.name,
            'account_id': product.property_account_income_id.id,
            'quantity': 1.0,
            'uom_id': product.uom_id.id,
            'price_unit': product.lst_price,
            'invoice_line_tax_id': product.taxes_id,
        }

        # if account_invoice_line_vals.get('invoice_line_tax_id', False):
        #     account_invoice_line_vals['invoice_line_tax_id'] = [
        #         (6, False, product.taxes_id)]
        #
        # quantity = len(self.env['account.payment.term'].read(
        #     cr, uid, payment_term_id, ['line_ids'], context=context)['line_ids'])
        # account_invoice_line_vals['quantity'] = quantity

        return account_invoice_line_vals

    @api.multi
    def invoice_validate(self):
        for invoice in self:
            pass

        # end for
        return super().invoice_validate()
    # end invoice_validate
