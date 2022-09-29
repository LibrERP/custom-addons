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
from odoo import models, fields, api, tools


class AccountMoveLineGroup(models.Model):
    _name = 'account.move.line.group'

    _auto = False
    # _rec_name = 'date_maturity'
    _order = "date_maturity_group desc"

    @api.multi
    # @api.depends('debit', 'credit')
    def _compute_running_balance(self):
        balance = 0
        for line in self:
            self.env.cr.execute('SELECT SUM(debit-credit) FROM account_move_line WHERE id = {line_id}'.format(
                line_id=line.id))
            line_balance = self.env.cr.fetchone()[0]
            balance += line_balance
            line.running_balance = balance

    # @api.depends('balance', 'payment_type')
    def _compute_color(self):
        for line in self:
            if line.payment_type:
                line.row_color = 'black'
                continue
            if line.balance > 0:
                line.row_color = 'green'
            else:
                line.row_color = 'red'

    partner_id = fields.Many2one('res.partner', 'Partner', select=1, ondelete='restrict')
    account_id = fields.Many2one('account.account', 'Account', required=True, ondelete="cascade")
    date_maturity_group = fields.Date('Data scadenza', select=True)
    balance = fields.Float(string='Saldo')
    payment_type = fields.Char('Tipo')
    state = fields.Char('State')
    blocked = fields.Boolean('Litigation')

    running_balance = fields.Float(
        compute=_compute_running_balance,
        string="Saldo progressivo",
        store=False
    )

    row_color = fields.Char(
        string='Row color',
        compute=_compute_color,
    )

    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'account_move_line_group')
        self.env.cr.execute("""
            create or replace view account_move_line_group as (
                SELECT 
                    min(A.id) AS id, 
                    A.partner_id,
                    A.account_id,
                    A.blocked,
                    A.date_maturity_group,
                    sum(A.balance) AS balance,
                    A.payment_type,
                    A.reconciled,
                    A.state
                    FROM( 
                        SELECT
                            min(aml.id) AS id, 
                            aml.partner_id,
                            aml.account_id,
                            aml.blocked,
                            CASE
                                WHEN aml.date_maturity IS NOT NULL THEN aml.date_maturity
                                ELSE aml.date
                            END AS date_maturity_group,

                            CASE
                                WHEN aml.reconciled IS NOT NULL THEN True
                                ELSE False 
                            END AS reconciled,
                            sum(aml.debit - aml.credit) AS balance,
                            apm.name AS payment_type,
                            am.state AS state
                        FROM account_move_line aml INNER JOIN account_account aa ON
                            aml.account_id = aa.id 
                            INNER JOIN account_move am ON 
                            aml.move_id = am.id
                            left join account_payment_method apm ON 
                            aml.payment_method = apm.id
                        WHERE 
                            aa.reconcile AND aml.partner_id is not NULL 
                            AND apm.code IS NOT NULL
                            AND apm.code IN (
                            'electronic',
                            'sdd-o',
                            'RB-o',
                            'riba_cbi'
                            )
                              
                        GROUP BY 
                            aml.partner_id, 
                            aml.account_id, 
                            aml.blocked, 
                            date_maturity_group, 
                            am.state, 
                            reconciled, 
                            apm.name

                        ) AS A
                        WHERE A.payment_type != '' 
                        GROUP BY 
                        A.date_maturity_group, 
                        A.partner_id, 
                        A.account_id, 
                        A.blocked, 
                        A.payment_type, 
                        A.reconciled, 
                        A.state
            )
        """)
