# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    tax_note = fields.Text(string="Note")
