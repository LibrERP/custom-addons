# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import timedelta

from pytz import timezone, utc

from odoo import models
from odoo.addons.resource.models.utils import HOURS_PER_DAY


class ResourceMixin(models.AbstractModel):
    _inherit = 'resource.mixin'

    def _list_work_time_per_day(self, from_datetime, to_datetime, calendar=None, domain=None):
        """When the ``weekend_included`` context flag is set, add the weekend
        days (Saturday and Sunday) contained in ``[from_datetime, to_datetime]``
        to the work-time list, so that they are counted in the leave duration.

        Weekend days already present (an unusual attendance configuration where
        the calendar works on the weekend) are left untouched, and the hours
        assigned to an added weekend day are the calendar's average hours per
        day.
        """
        result = super()._list_work_time_per_day(
            from_datetime, to_datetime, calendar=calendar, domain=domain)
        if not self.env.context.get('weekend_included'):
            return result

        # naive datetimes are made explicit in UTC, mirroring the base method
        if not from_datetime.tzinfo:
            from_datetime = from_datetime.replace(tzinfo=utc)
        if not to_datetime.tzinfo:
            to_datetime = to_datetime.replace(tzinfo=utc)

        for record in self:
            record_calendar = calendar or record.resource_calendar_id \
                or record.company_id.resource_calendar_id
            if not record_calendar:
                continue
            tz = timezone(record_calendar.tz) if record_calendar.tz else utc
            weekend_hours = record_calendar.hours_per_day or HOURS_PER_DAY

            work_time = dict(result.get(record.id, []))
            current_date = from_datetime.astimezone(tz).date()
            end_date = to_datetime.astimezone(tz).date()
            while current_date <= end_date:
                # 5 = Saturday, 6 = Sunday
                if current_date.weekday() >= 5 and current_date not in work_time:
                    work_time[current_date] = weekend_hours
                current_date += timedelta(days=1)
            result[record.id] = sorted(work_time.items())
        return result
