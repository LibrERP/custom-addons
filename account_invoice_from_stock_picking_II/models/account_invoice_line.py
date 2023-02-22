# © 2022-2023 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models, api


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    def set_price_unit(self):
        if not self.product_id:
            return
        params = {'invoice_id': self.invoice_id}
        seller = self.product_id._select_seller(
            partner_id=self.partner_id,
            quantity=self.quantity,
            date=self.invoice_id.date_invoice,
            uom_id=self.uom_id,
            params=params)

        if not seller:
            if self.product_id.seller_ids.filtered(lambda s: s.name.id == self.partner_id.id):
                self.price_unit = 0.0
            return

        price_unit = self.env['account.tax']._fix_tax_included_price_company(seller.price, self.product_id.supplier_taxes_id, self.invoice_line_tax_ids, self.company_id) if seller else 0.0
        if price_unit and seller and self.invoice_id.currency_id and seller.currency_id != self.invoice_id.currency_id:
            price_unit = seller.currency_id._convert(
                price_unit, self.invoice_id.currency_id, self.invoice_id.company_id, self.date_invoice or fields.Date.today())

        if seller and self.uom_id and seller.product_uom.id != self.uom_id.id:
            price_unit = seller.product_uom._compute_price(price_unit, self.uom_id)

        self.price_unit = price_unit

    def unlink(self):
        for invoice_line in self:
            for stock_move in invoice_line.move_line_ids:
                stock_move.invoiced = False
                if not stock_move.picking_id.move_ids_without_package.filtered(
                    lambda r: r.invoiced == True
                ):
                    stock_move.picking_id.invoice_state = '2binvoiced'

        return super().unlink()
