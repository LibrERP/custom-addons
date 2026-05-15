# © 2020-2023 Fabio Colognesi - Didotech srl
# © 2024-2026 Fabio Colognesi - Codebeex srl (www.codebeex.com)
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect

from odoo import api, fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    region_id = fields.Many2one("res.country.region", string='Region', ondelete='restrict', domain="[('country_id', '=?', country_id)]")

    @api.onchange('state_id')
    def on_change_state_id(self):
        if self.state_id:
            self.region_id = self.state_id.region_id
