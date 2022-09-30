##############################################################################
#
#    Copyright (C) 2022 Didotech SRL
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.multi
    @api.depends('debit', 'credit')
    def _compute_running_balance(self):
        balance = 0
        for line in self:
            self.env.cr.execute('SELECT SUM(debit-credit) FROM account_move_line WHERE id = {line_id}'.format(
                line_id=line.id))
            line_balance = self.env.cr.fetchone()[0]
            balance += line_balance
            line.running_balance = balance

    running_balance = fields.Float(
        compute=_compute_running_balance,
        string="Saldo progressivo",
        store=False
    )
