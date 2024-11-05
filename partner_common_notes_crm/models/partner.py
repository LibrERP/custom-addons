# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
from email.policy import default

from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    common_note_ids = fields.One2many(
        'mail.message', inverse_name='partner_id', string='Messages',
        domain=lambda self: [
            ('message_type', 'in', ('comment', 'notification', 'email')),
            ('body', '!=', ''),
            ('model', 'like', self.note_filter)],
        auto_join=True)

    note_filter = fields.Selection([
        ('sale.order', 'Sale Orders'),
        ('crm.lead', 'Leads'),
        ('%', 'All'),
    ], default='%')
