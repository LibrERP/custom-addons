# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _l10n_it_edi_send(self, attachments_vals):
        return True
