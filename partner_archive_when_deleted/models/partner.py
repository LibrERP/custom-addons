# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def unlink(self):
        self.active = False
