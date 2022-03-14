# © 2022 - Didotech srl <https://www.didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields, _

import platform


class CompanyConfig(models.Model):
    _inherit = "res.company"

    def _get_node(self):
        self.local_node = platform.node()

    email_node = fields.Char(
        'Email Host', size=64, required=True, default='Some Node',
        help="To be able to send Emails this value should be"
             "equal to the name of the local host")
    local_node = fields.Char(compute=_get_node, string='Local Host', method=True)


class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    email_node = fields.Char(
        related='company_id.email_node',
        string='Email Host',
        readonly=False,
        help="To be able to send Emails this value should be equal to the name of the local host"
    )
    local_node = fields.Char(related='company_id.local_node', string='Local Host', readonly=True)
