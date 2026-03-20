# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    def message_update(self, msg_dict, update_vals=None):
        ticket = super().message_update(msg_dict, update_vals)

        # Detect inbound email (important!)
        if msg_dict.get('type') == 'email':
            author_id = msg_dict.get('author_id')

            # Optional: avoid internal users
            if not self.env['res.users'].sudo().search([('partner_id', '=', author_id)]):
                new_stage = self._get_reopen_stage()
                if new_stage:
                    ticket.stage_id = new_stage.id

        return ticket

    def _get_reopen_stage(self):
        param = self.env['ir.config_parameter'].sudo()
        stage_id = param.get_param('helpdesk.reply_stage_id')

        if stage_id:
            stage = self.env['helpdesk.ticket.stage'].browse(int(stage_id))
            if stage.exists():
                return stage

        return False
