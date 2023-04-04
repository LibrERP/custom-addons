# © 2023 Didotech s.r.l.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AgedPartnerBalanceWizard(models.TransientModel):
    """Aged partner balance report wizard."""

    _inherit = 'aged.partner.balance.wizard'
    _description = 'Aged Partner Balance Wizard'

    hide_account_at_0 = fields.Boolean(
        string='Nascondi righe con saldo finale a 0',
    )

    def _prepare_report_aged_partner_balance(self):
        self.ensure_one()
        res = super()._prepare_report_aged_partner_balance()
        res['hide_account_at_0'] = self.hide_account_at_0
        return res

