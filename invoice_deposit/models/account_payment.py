# Didotech srl 2023
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.addons.account.models.account_payment import (
    MAP_INVOICE_TYPE_PAYMENT_SIGN,
)


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.model
    def default_get(self, fields):
        """
        Compute amount to pay according to deposit
        """
        rec = super(AccountPayment, self).default_get(fields)
        invoice_defaults = self.resolve_2many_commands(
            'invoice_ids', rec.get('invoice_ids')
        )
        if invoice_defaults and len(invoice_defaults) == 1:
            invoice = invoice_defaults[0]
            if (
                'has_deposit' in invoice
                and invoice['has_deposit']
            ):
                rec['amount'] = invoice['amount_net_pay']
        return rec

    @api.multi
    def _compute_payment_amount(self, invoices=None, currency=None):
        '''Compute the total amount for the payment wizard.

        :param invoices: If not specified, pick all the invoices.
        :param currency: If not specified, search a default currency on wizard/journal.
        :return: The total amount to pay the invoices.
        '''

        # Get the payment invoices
        if not invoices:
            invoices = self.invoice_ids

        # Get the payment currency
        payment_currency = currency
        if not payment_currency:
            payment_currency = (
                self.currency_id
                or self.journal_id.currency_id
                or self.journal_id.company_id.currency_id
                or invoices
                and invoices[0].currency_id
            )
        total = 0.0

        for inv in invoices:
            if inv.has_deposit:
                total += inv.residual
            else:
                total += self._compute_payment_invoice(inv, payment_currency)
        return total

    @api.model
    def _compute_payment_invoice(self, invoice, currency):
        total = 0.0
        payment_currency = currency

        res = super()._compute_payment_invoice(invoice, currency)
        if not payment_currency:
            payment_currency = (
                self.currency_id
                or self.journal_id.currency_id
                or self.journal_id.company_id.currency_id
                or invoice.currency_id
            )
        sign = MAP_INVOICE_TYPE_PAYMENT_SIGN[invoice.type]

        amount_total = sign * invoice.residual_signed
        amount_total_company_signed = sign * invoice.residual_company_signed
        invoice_currency = self.env['res.currency'].browse(
            invoice.currency_id.id
        )
        if (
            getattr(invoice, 'withholding_tax_amount', False)
            and invoice.withholding_tax_amount
        ):
            amount_total = sign * invoice.amount_net_pay_residual
            # amount_total_company_signed = sign * invoice.amount_net_pay_residual
        # and if

        if payment_currency == invoice_currency:
            total += amount_total
        else:

            total += self.journal_id.company_id.currency_id._convert(
                amount_total_company_signed,
                payment_currency,
                self.env.user.company_id,
                self.payment_date or fields.Date.today(),
            )
        # end if

        return total

    # end _compute_payment_invoice