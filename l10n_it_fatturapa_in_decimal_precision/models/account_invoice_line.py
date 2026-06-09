# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    fatturapa_xml_imported = fields.Boolean(
        string="Imported from FatturaPA XML",
        help="When set, price_subtotal/price_total are computed from the "
             "original XML values (fatturapa_xml_*) instead of the live "
             "form values, which may be rounded to the current display "
             "precision. Untick to allow manual editing.",
    )
    fatturapa_xml_price_unit = fields.Float(
        string="XML Unit Price",
        digits=(16, 8),
    )
    fatturapa_xml_quantity = fields.Float(
        string="XML Quantity",
        digits=(16, 8),
    )
    fatturapa_xml_discount = fields.Float(
        string="XML Discount (%)",
        digits=(16, 8),
    )

    @api.one
    @api.depends(
        'price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
        'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id',
        'invoice_id.company_id', 'invoice_id.date_invoice', 'invoice_id.date',
        'fatturapa_xml_imported', 'fatturapa_xml_price_unit',
        'fatturapa_xml_quantity', 'fatturapa_xml_discount',
    )
    def _compute_price(self):
        if not self.fatturapa_xml_imported:
            return super()._compute_price()

        currency = self.invoice_id and self.invoice_id.currency_id or None
        price_unit = self.fatturapa_xml_price_unit
        quantity = self.fatturapa_xml_quantity
        discount = self.fatturapa_xml_discount or 0.0
        price = price_unit * (1 - discount / 100.0)
        taxes = False
        if self.invoice_line_tax_ids:
            taxes = self.invoice_line_tax_ids.compute_all(
                price, currency, quantity,
                product=self.product_id,
                partner=self.invoice_id.partner_id,
            )
        self.price_subtotal = price_subtotal_signed = (
            taxes['total_excluded'] if taxes else quantity * price
        )
        self.price_total = (
            taxes['total_included'] if taxes else self.price_subtotal
        )
        if (
            self.invoice_id.currency_id
            and self.invoice_id.currency_id != self.invoice_id.company_id.currency_id
        ):
            currency = self.invoice_id.currency_id
            date = self.invoice_id._get_currency_rate_date()
            price_subtotal_signed = currency._convert(
                price_subtotal_signed,
                self.invoice_id.company_id.currency_id,
                self.company_id or self.env.user.company_id,
                date or fields.Date.today(),
            )
        sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
        self.price_subtotal_signed = price_subtotal_signed * sign
