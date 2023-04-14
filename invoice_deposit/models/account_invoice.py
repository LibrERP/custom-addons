# Didotech srl 2023
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    deposit = fields.Monetary(string="Caparra", default=0.0,)
    has_deposit = fields.Boolean(string="Ha la caparra", default=False)

    @api.onchange('set_deposit')
    def onchange_set_deposit(self):
        if self.state == 'draft':
            if self.has_deposit is False:
                self.deposit = 0.00

    @api.depends('amount_total')
    def _compute_net_pay(self):
        super()._compute_net_pay()
        for inv in self:
            inv.amount_net_pay = inv.amount_total
            if inv.has_deposit:
                inv.amount_net_pay -= inv.deposit
                inv.amount_net_pay_residual -= inv.deposit

    @api.multi
    def write(self, values):

        result = super().write(values)

        # Set default values, but avoid the "infinite
        # recursive calls to write" issue
        if not self.env.context.get('StopRecursion'):

            # Set context variable to stop recursion
            self = self.with_context(StopRecursion=True)

            for invoice in self:

                if invoice.state == 'draft':
                    if 'deposit' in values and 'has_deposit' in values and values['has_deposit'] is True:
                        if values['deposit'] > invoice.amount_total:
                            raise UserError(
                                'Attenzione\nLa caparra deve essere minore dell\'importo totale della fattura.')
                    invoice.update_duedates()
                # end if

            # end for

        # end if "StopRecursion"
        return result

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if 'has_deposit' in vals and 'deposit' in vals:
            if vals['deposit'] > res.amount_total:
                raise UserError('Attenzione\nLa caparra deve essere minore dell\'importo totale della fattura.')
        return res

    @api.one
    @api.depends(
        'state', 'currency_id', 'invoice_line_ids.price_subtotal',
        'move_id.line_ids.amount_residual',
        'move_id.line_ids.currency_id')
    def _compute_residual(self):
        res = super()._compute_residual()
        residual = 0.0
        residual_company_signed = 0.0
        sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
        for line in self._get_aml_for_amount_residual():
            residual_company_signed += line.amount_residual
            if line.currency_id == self.currency_id:
                residual += line.amount_residual_currency if line.currency_id else line.amount_residual
            else:
                if line.currency_id:
                    residual += line.currency_id._convert(line.amount_residual_currency, self.currency_id, line.company_id, line.date or fields.Date.today())
                else:
                    residual += line.company_id.currency_id._convert(line.amount_residual, self.currency_id, line.company_id, line.date or fields.Date.today())

        if self.has_deposit:
            self.residual = abs(residual - self.deposit)

        self.residual_company_signed = abs(residual_company_signed - self.deposit) * sign
        self.residual_signed = abs(residual  - self.deposit) * sign
        digits_rounding_precision = self.currency_id.rounding
        if float_is_zero(self.residual, precision_rounding=digits_rounding_precision):
            self.reconciled = True
        else:
            self.reconciled = False

