# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.onchange('is_move_sent')
    def onchange_is_move_sent(self):
        for move in self:
            if move.is_move_sent:
                move.l10n_it_edi_state = 'being_sent'
            else:
                move.l10n_it_edi_state = ''
