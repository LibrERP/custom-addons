# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if not version:
        return
    cr.execute(
        """
        UPDATE ateco_category
        SET active = FALSE
        WHERE active = TRUE
          AND id NOT IN (
              SELECT res_id
              FROM ir_model_data
              WHERE model = 'ateco.category'
                AND module = 'l10n_it_ateco_plus'
                AND res_id IS NOT NULL
          )
        """
    )
    _logger.info(
        "l10n_it_ateco_plus: recovery migration deactivated %s non-plus ateco.category records",
        cr.rowcount,
    )