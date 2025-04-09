# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # 1.2.6 RiferimentoAmministrazione
    l10n_it_partner_code = fields.Char("PA Code for Partner", size=20, required=False, default="")

    def _l10n_it_edi_get_values(self):
        values = super()._l10n_it_edi_get_values()
        if self and len(self) == 1:
            values['l10n_it_partner_code'] = self.l10n_it_partner_code

        return values
