# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    l10n_it_pec_email = fields.Char(string="PEC e-mail")
