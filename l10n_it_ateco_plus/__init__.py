import logging

from . import models

_logger = logging.getLogger(__name__)


def pre_init_deactivate_ateco_categories(env):
    # This function is executed before the first installation of the module (only)
    env.cr.execute(
        "ALTER TABLE ateco_category "
        "ADD COLUMN IF NOT EXISTS active BOOLEAN DEFAULT TRUE"
    )
    env.cr.execute("UPDATE ateco_category SET active = FALSE")
    _logger.info(
        "l10n_it_ateco_plus: pre_init deactivated %s pre-existing ateco.category records",
        env.cr.rowcount,
    )
