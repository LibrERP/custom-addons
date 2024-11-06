# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models


class CrmTeam(models.Model):
    _inherit = "crm.team"

    lead_color = fields.Selection(
        [
            ('white', 'White'),
            ('lightgreen', 'Green'),
            ('lightblue', 'Blue'),
            ('lightyellow', 'Yellow'),
            ('lightgrey', 'Grey'),
            ('black', 'Black'),
        ], string='Lead Color',
        default='white'
    )
