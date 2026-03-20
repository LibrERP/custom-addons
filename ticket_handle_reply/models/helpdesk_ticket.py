# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models

import logging
logger = logging.getLogger(__name__)


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    def message_post(self, **kwargs):
        # logger.info('--1-- Message post')
        message = super().message_post(**kwargs)

        if not message:
            return message

        if message.message_type == 'email':
            # logger.info('--2-- Type: Email')
            for ticket in self:
                stage = ticket._get_reopen_stage()
                # logger.info(f'--3-- New stage: {stage.name}')
                if stage:
                    # logger.info(f"--4-- Setting New stage...")
                    ticket.stage_id = stage.id

        return message

    def _get_reopen_stage(self):
        param = self.env['ir.config_parameter'].sudo()
        stage_id = param.get_param('helpdesk.reply_stage_id')

        if stage_id:
            stage = self.env['helpdesk.ticket.stage'].browse(int(stage_id))
            if stage.exists():
                return stage

        return False
