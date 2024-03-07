# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ddt_note = fields.Text('DDT Note', help=_("This note will be printed in the DDT"))
    ddt_internal_note = fields.Text('DDT Internal Note', help=_("This note is not printed in the DDT"))
