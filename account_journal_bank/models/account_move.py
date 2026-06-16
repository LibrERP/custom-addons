# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.depends("journal_id.payment_bank_id", "invoice_payment_term_id.riba")
    def _compute_partner_bank_id(self):
        super()._compute_partner_bank_id()
        for move in self:
            term = move.invoice_payment_term_id
            if (
                move.is_sale_document(include_receipts=True)
                and move.journal_id.payment_bank_id
                and not term.riba
                and not getattr(term, "already_paid", False)
            ):
                move.partner_bank_id = move.journal_id.payment_bank_id
