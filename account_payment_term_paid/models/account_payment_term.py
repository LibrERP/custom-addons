# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"

    already_paid = fields.Boolean(
        string="Already Paid",
        help="If checked, invoices using this payment term are treated as "
             "already settled and no payment info (e.g. bank account) is set.",
    )
