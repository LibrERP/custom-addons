# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    # Extend the recompute triggers of ``number_of_days`` / ``number_of_hours``
    # so that toggling ``weekend_included`` on the leave type re-runs the
    # duration computation. An overriding ``@api.depends`` fully replaces the
    # trigger set of the compute method (it is not merged), so the base
    # dependencies are repeated here alongside the new one.
    @api.depends('date_from', 'date_to', 'resource_calendar_id',
                 'holiday_status_id.request_unit', 'holiday_status_id.weekend_included')
    def _compute_duration(self):
        super()._compute_duration()

    def _get_durations(self, check_leave_type=True, resource_calendar=None):
        """Split the leaves by their leave type ``weekend_included`` flag so
        that the flag can be propagated to ``_list_work_time_per_day`` through
        the context.

        Grouping is required because ``_get_durations`` batches employees by
        ``(date_from, date_to, ..., calendar)``: two leaves sharing those keys
        but belonging to leave types with a different ``weekend_included`` value
        must not share the same computed work-time result.
        """
        result = {}
        for weekend_included in (True, False):
            leaves = self.filtered(
                lambda leave: bool(leave.holiday_status_id.weekend_included) == weekend_included
            )
            if not leaves:
                continue
            result.update(
                super(
                    HrLeave,
                    leaves.with_context(weekend_included=weekend_included),
                )._get_durations(
                    check_leave_type=check_leave_type,
                    resource_calendar=resource_calendar,
                )
            )
        return result
