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

                        # end if
                    # end if

                    if 'has_deposit' in values and values['has_deposit'] is True or invoice.has_deposit:
                        invoice.action_update_duedates_and_move_lines()
                # end if

            # end for

        # end if "StopRecursion"
        return result

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if 'has_deposit' in vals and vals['has_deposit'] is True and 'deposit' in vals:
            if vals['deposit'] > res.amount_total:
                raise UserError('Attenzione\nLa caparra deve essere minore dell\'importo totale della fattura.')
            self.update_duedates()
        return res

    def _get_aml_for_amount_residual(self):
        """ Get the aml to consider to compute the amount residual of invoices """
        self.ensure_one()
        res = super()._get_aml_for_amount_residual()
        if self.has_deposit:
            return self.sudo().move_id.line_ids.filtered(lambda l: l.account_id == self.account_id and l.payment_method.code != 'tax')
        else:
            return res
    #
    @api.multi
    def _get_aml_caparra_for_register_payment(self):
        """ Get the aml caparra to consider to reconcile in register payment """
        self.ensure_one()
        res = super()._get_aml_for_register_payment()
        return self.sudo().move_id.line_ids.filtered(lambda l: l.account_id == self.account_id and l.payment_method.code == 'tax')

    @api.multi
    def register_payment(self, payment_line, writeoff_acc_id=False, writeoff_journal_id=False):
        """ Reconcile payable/receivable lines from the invoice with payment_line """
        line_to_reconcile = self.env['account.move.line']
        for inv in self:
            # se ha una caparra e non è stata riconciliata
            line = inv._get_aml_caparra_for_register_payment()
            if inv.has_deposit and payment_line.credit == inv.deposit and line and line.reconciled is False:
                line_to_reconcile += line
            else:
                line_to_reconcile += inv._get_aml_for_register_payment()
        # return super().register_payment(payment_line, writeoff_acc_id, writeoff_journal_id)
        return (line_to_reconcile + payment_line).reconcile(writeoff_acc_id, writeoff_journal_id)

