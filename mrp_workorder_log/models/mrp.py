# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models, _


class FormattedTime:
    # days: int
    # hours: int
    minutes: int
    seconds: int

    def __init__(self, value):
        # self.days = int(value / 24)
        # self.hours = int(value % 24)
        # self.minutes = value % 24 % 1 * 60
        self.minutes = int(value)
        self.seconds = round(value % 1 * 60)

    def __str__(self):
        return f"{self.minutes}:{self.seconds:02d}"


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    def write(self, values):
        if 'duration' in values:
            self.production_id.message_post(
                body=f"{self.name}: The Real Duration was changed from {FormattedTime(self.duration)} to {FormattedTime(values['duration'])}"
            )
        return super().write(values)
