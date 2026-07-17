# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    """Recompute the duration of existing leaves whose type includes weekends.

    ``weekend_included`` was not part of the ``_compute_duration`` triggers in
    the first release, so leaves created before this upgrade kept a duration
    that excluded the weekend days.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    leaves = env['hr.leave'].search([
        ('holiday_status_id.weekend_included', '=', True),
    ])
    if leaves:
        leaves._compute_duration()
