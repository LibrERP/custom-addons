# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    # `login_date` is a related field on res.users.log, which regular users are
    # not allowed to read. This computed field exposes the same value through
    # sudo() so the list can be shown to every user.
    last_access_time = fields.Datetime(
        string='Last Access Time',
        compute='_compute_last_access_time',
    )

    @api.depends('login_date')
    def _compute_last_access_time(self):
        for user in self:
            user.last_access_time = user.sudo().login_date
