# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models


class MailMessage(models.Model):
    _inherit = "mail.message"

    partner_id = fields.Many2one(comodel_name='res.partner', compute='_compute_partner', store=True)
    body_html = fields.Html(compute='_compute_body_html', string='Notes')

    @api.depends('model', 'res_id')
    def _compute_partner(self):
        for messsage in self:
            if messsage.res_id:
                record = self.env[messsage.model].browse(messsage.res_id)
                if hasattr(record, 'partner_id'):
                    messsage.partner_id = record.partner_id.id
                else:
                    messsage.partner_id = False
            else:
                messsage.partner_id = False

    def _compute_body_html(self):
        for message in self:
            if message.body and message.partner_id:
                message.body_html = f"""
                <img src="/web/image/res.partner/{message.author_id.id}/image_small" 
                style="border-radius: 30px; margin-left: 12px; margin-top: 3px;" 
                height="36" width="36">
                <div style="color: #adb5bd; margin-left: 60px; margin-top: -40px;">Note by <strong>{message.author_id.name}</strong> - {message.date.date()}</div></br>
                <div style="margin-left: 60px;">{message.body}</div>
                """
