from . import models


def post_init_hook(env):
    """Recompute the duration of already-existing leaves whose type includes
    weekends, so that historical records (created before this module was
    installed or before the flag was enabled) reflect the new calculation."""
    leaves = env['hr.leave'].search([
        ('holiday_status_id.weekend_included', '=', True),
    ])
    if leaves:
        leaves._compute_duration()
