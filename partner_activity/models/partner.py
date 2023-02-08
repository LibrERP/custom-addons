# © 2023 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    all_activity_ids = fields.One2many(
        'mail.activity', 'partner_id', 'Activities',
        groups="base.group_user", readnoly=True)
