# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    is_pec = fields.Boolean("PEC Server")
