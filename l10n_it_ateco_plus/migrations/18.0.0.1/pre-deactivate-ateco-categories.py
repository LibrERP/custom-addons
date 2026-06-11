# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if not version:
        return
    cr.execute("UPDATE ateco_category SET active = FALSE")
    _logger.info(
        "l10n_it_ateco_plus: deactivated %s ateco.category records before loading new data",
        cr.rowcount,
    )