# Didotech srl 2023
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import UserError


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
