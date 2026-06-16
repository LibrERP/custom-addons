# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    payment_bank_id = fields.Many2one(
        comodel_name="res.partner.bank",
        string="Beneficiary Bank",
        domain="[('partner_id', '=', company_partner_id)]",
    )
