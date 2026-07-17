# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HolidaysType(models.Model):
    _inherit = 'hr.leave.type'

    weekend_included = fields.Boolean(
        string='Weekend Included',
        default=False,
        help="Weekend days (Saturday and Sunday) falling inside the requested "
             "period are counted in the leave duration. Useful for leaves "
             "whose legal duration is expressed in calendar days rather than "
             "working days (e.g. marriage leave).",
    )
