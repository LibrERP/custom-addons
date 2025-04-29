# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    @api.depends("account_edi_proxy_client_ids")
    def _compute_l10n_it_edi_proxy_user_id(self):
        for company in self:
            company.l10n_it_edi_proxy_user_id = company.account_edi_proxy_client_ids.filtered(lambda x: x.proxy_type == 'dummy')
