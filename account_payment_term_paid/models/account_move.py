# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.depends("invoice_payment_term_id.already_paid")
    def _compute_partner_bank_id(self):
        super()._compute_partner_bank_id()
        for move in self:
            if move.invoice_payment_term_id.already_paid:
                move.partner_bank_id = False
