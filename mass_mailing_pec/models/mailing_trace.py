# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class ModelModel(models.Model):
    _inherit = "mailing.trace"

    # trace_status = fields.Selection(
    #     selection_add=[
    #         ('acceptance', 'Accettazione'),  # Always returned, even if destination is not PEC
    #         ('acknowledgement-delivery', 'Avvenuta-Consegna')  # Returns when message reach the destination server
    #     ]
    # )

    pec_status = fields.Selection(selection=[
        ('new', ''),
        ('acceptance', 'Accettazione'),  # Always returned, even if destination is not PEC
        ('acknowledgement-delivery', 'Avvenuta-Consegna')  # Returns when message reach the destination server
    ])


