# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.onchange('payment_mode_id')
    def onchange_payment_mode_id(self):
        if self.payment_mode_id:
            self.partner_bank_id = self.payment_mode_id.fixed_journal_id.bank_account_id.id

    @api.model_create_multi
    def create(self, values):
        for vals in values:
            if not vals.get('partner_bank_id'):
                partner = self.env['res.partner'].browse(vals['partner_id'])
                if partner.customer_payment_mode_id:
                    if vals.get('payment_mode_id', False):
                        payment_mode = self.env['account.payment.mode'].browse(vals['payment_mode_id'])
                        if (payment_mode.bank_account_link == 'fixed' and
                                payment_mode.payment_method_id.code == 'manual'):
                            vals['partner_bank_id'] = \
                               payment_mode.fixed_journal_id.bank_account_id.id
                    else:
                        vals['payment_mode_id'] = partner.customer_payment_mode_id.id
                        if (partner.customer_payment_mode_id.bank_account_link == 'fixed' and
                                partner.customer_payment_mode_id.payment_method_id.code == 'manual'):
                            vals['partner_bank_id'] = \
                                partner.customer_payment_mode_id.fixed_journal_id.bank_account_id.id

        return super().create(values)
