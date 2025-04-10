# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # 1.2.6 RiferimentoAmministrazione
    l10n_it_partner_code = fields.Char(
        "Riferimento Amministrazione",
        size=20,
        required=False,
        default="",
        help="1.2.6 <RiferimentoAmministrazione>"
    )
