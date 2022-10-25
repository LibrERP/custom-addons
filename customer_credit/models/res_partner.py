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
import time
from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime, timedelta


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _search_overdue_credit(self, operator, value):
        if not value:
            value = 0
        current_date = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
        sql = """
            SELECT partner_id
            FROM 
            (
                  SELECT 
                        account_move_line.partner_id,
                        SUM(account_move_line.debit) - SUM(account_move_line.credit) as overdue
        
                  FROM 
                      account_account, 
                      account_move,
                      account_move_line,
                      res_partner
                  WHERE 
                      account_move_line.account_id = account_account.id AND
                      account_move_line.partner_id = res_partner.id AND
                      (res_partner.collections_out != 'True' OR res_partner.collections_out IS NULL) AND
                      account_move_line.move_id = account_move.id AND
                      account_move.state != 'draft' AND 
                      account_account.user_type_id IN (
                      SELECT id FROM account_account_type WHERE type  = 'receivable') AND 
                      account_move_line.reconciled IS NULL AND
                      account_move_line.date_maturity <= '{dat}' 
                  GROUP BY
                      account_move_line.partner_id
            ) AS scaduto
            WHERE 
                scaduto.overdue {ope} {val}
                          
          """.format(
            dat=current_date,
            ope=operator,
            val=value
        )
        self.env.cr.execute(sql)

        res = self.env.cr.fetchall()
        partner_ids = []
        if res:
            partner_ids = [x[0] for x in res]

        if not partner_ids:
            return [('id', '=', 0)]
        return [('id', 'in', list(set(partner_ids)))]

    @api.depends('credit_limit')
    def _compute_fido(self):

        for record in self:
            draft_invoices_amount = 0.0
            orders_amount = 0.0
            riba_amount = 0.0
            # credit = impostato - impegnato
            # impostato = credit_limit
            # impegnato

            # note di carico pagate
            domain = list()
            domain.append(('partner_id', '=', record.id))
            domain.append(('amount_paid', '>', 0))
            shopping_orders = record.env['sale.order'].search(domain)

            for order in shopping_orders:
                orders_amount += order.amount_total

            # resi ?
            domain = list()
            domain.append(('partner_id', '=', record.id))
            domain.append(('returned_by', '=', True))
            domain.append(('credit_note', '!=', False))
            # domain.append(('invoice_ids', '=', False)) # ??
            pickings = record.env['stock.picking'].search(domain)

            for picking in pickings:
                credit_note = picking.credit_note
                orders_amount -= credit_note.amount_total

            # fatture in bozza
            domain = list()
            domain.append(('partner_id', '=', record.id))
            domain.append(('type', '=', 'out_invoice'))
            domain.append(('state', '=', 'draft'))
            draft_out_invoices_ids = record.env['account.invoice'].search(domain)

            for invoice in draft_out_invoices_ids:
                draft_invoices_amount += invoice.amount_total

            # note di credito in bozza
            domain = list()
            domain.append(('partner_id', '=', record.id))
            domain.append(('type', '=', 'out_refund'))
            domain.append(('state', '=', 'draft'))
            draft_refound_invoices_ids = record.env['account.invoice'].search(domain)

            for invoice in draft_refound_invoices_ids:
                draft_invoices_amount -= invoice.amount_total

            # riba
            filter_date = (datetime.now() - timedelta(days=2)).strftime(DEFAULT_SERVER_DATE_FORMAT)
            domain = list()
            domain.append(('partner_id', '=', record.id))
            domain.append(('reconciled', '=', True))
            domain.append(('payment_method.code', '=', 'riba_cbi'))
            domain.append(('date_maturity', '>', filter_date))
            aml_riba = record.env['account.move.line'].search(domain)

            for line in aml_riba:
                riba_amount += line.balance

            approved_pos_amount = 0.0
            domain = list()
            domain.append(('partner_id', '=', record.id))
            domain.append(('to_be_invoiced', '=', True))
            domain.append(('invoice_id', '=', False))
            # domain.append(('invoice_ids', '=', False)) # ??
            ddts = record.env['stock.picking.package.preparation'].search(domain)
            for ddt in ddts:
                for pick in ddt.picking_ids:
                    if pick.returned_by:
                        continue
                    order = pick.sale_id
                    if order:
                        # 19/10/2022 `sudo()` added to prevent access error if user has only Own Documents perm on sales
                        approved_pos_amount += order.sudo()['amount_total']

            record.fido_utilizzato = record.credit + draft_invoices_amount + orders_amount + riba_amount
            record.fido_residuo = record.credit_limit - (
                    record.credit + draft_invoices_amount + orders_amount + riba_amount)
            record.fatture_draft = draft_invoices_amount
            record.saldo_contabile = record.debit - record.credit
            record.esposizione_sbf = riba_amount
            record.ddt_to_invoice = approved_pos_amount

    def _compute_overdue_credit(self):
        current_date = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
        for partner in self:
            self.env.cr.execute("""SELECT
                                       account_move_line.partner_id,
                                       SUM(account_move_line.debit) - SUM(account_move_line.credit) as overdue
                                   FROM
                                       account_account,
                                       account_account_type,
                                       account_move_line,
                                       account_move
                                   WHERE
                                       account_account.user_type_id = account_account_type.id AND
                                       account_move_line.account_id = account_account.id AND
                                       account_move_line.move_id = account_move.id AND
                                       account_move.state != 'draft' AND
                                       account_account_type.type = 'receivable' AND
                                       account_move_line.reconciled IS NULL AND
                                       account_move_line.partner_id = %s AND
                                       (account_move_line.date_maturity <= %s 
                                           OR
                                       account_move_line.date <= %s AND account_move_line.date_maturity IS NULL)
    
                                   GROUP BY
                                       account_move_line.partner_id;
                               """, (partner.id, current_date, current_date))
            res_sql = self.env.cr.fetchall()

            for res_id in res_sql:
                partner.overdue_credit = res_id[1]

    fido_utilizzato = fields.Float(
        string='Fido utilizzato',
        compute=_compute_fido,
    )

    fido_residuo = fields.Float(
        string='Fido residuo',
        compute=_compute_fido,
    )

    saldo_contabile = fields.Float(
        string='Saldo Contabile',
        compute=_compute_fido,
    )

    fatture_draft = fields.Float(
        string='Fatture da Registrare',
        compute=_compute_fido,
    )

    esposizione_sbf = fields.Float(
        string='Esposizione SBF',
        compute=_compute_fido,
    )

    limit_note = fields.Text(
        string='Note fido'
    )

    blacklist = fields.Boolean(
        string='Utente bloccato',
        default=False,
    )

    validate = fields.Boolean(
        string='Validazione partner',
        default=False,
    )

    ddt_to_invoice = fields.Float(
        string='DDT da fatturare',
        compute=_compute_fido,
    )

    overdue_credit = fields.Float(
        string='Totale Scaduto',
        compute=_compute_overdue_credit,
        search=_search_overdue_credit,
        # store=True,
    )

    collections_out = fields.Boolean(
        string='Recupero Presso Terzi',
        default=False,
    )

    excluding_recall = fields.Boolean(
        string='Escluso dai richiami',
        default=False,
    )

