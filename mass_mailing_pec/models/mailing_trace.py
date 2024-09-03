# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class ModelModel(models.Model):
    _inherit = "mailing.trace"

    pec_status = fields.Selection(selection=[
        ('accettazione', 'Accettazione'),  # Always returned, even if destination is not PEC
        ('avvenuta-consegna', 'Avvenuta-Consegna')  # Returns when message reach the destination server
    ])
    message_id = fields.Char(string='Message-ID', index=True)
