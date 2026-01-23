# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    city_holiday_id = fields.Many2one(
        comodel_name='hr.holidays.public.line',
        string="City Holiday",
        # domain=[('city_id', '!=', False)]
        domain=[('year_id.year', '=', 1900)]
    )
