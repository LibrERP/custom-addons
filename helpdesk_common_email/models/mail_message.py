# © 2022 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models, modules, SUPERUSER_ID, tools


class Message(models.Model):
    _inherit = 'mail.message'

    @api.model
    def create(self, values):
        if values.get('model', False) == 'helpdesk.ticket' and values.get('message_type', '') == 'comment':
            ICP = self.env['ir.config_parameter'].sudo()
            values['email_from'] = ICP.get_param("helpdesk.email")

        return super().create(values)
