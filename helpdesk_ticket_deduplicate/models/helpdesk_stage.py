# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class HelpdeskStage(models.Model):
    _inherit = 'helpdesk.stage'

    is_cancel = fields.Boolean(
        string='Cancelled',
        help="Tickets in this stage are considered cancelled: they are not "
             "reported as duplicates, nor do they make other tickets look "
             "duplicated.",
    )
