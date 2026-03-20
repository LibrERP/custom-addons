# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    reply_stage_id = fields.Many2one(
        'helpdesk.ticket.stage',
        string="Move ticket to Stage",
        config_parameter='helpdesk.reply_stage_id',
    )
