##############################################################################
#
#    Copyright (C) 2022-2023 Didotech SRL
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
                      account_move_line.reconciled = 'false' AND
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
            if record.id:
                draft_invoices_amount = 0.0
                orders_amount = 0.0
                riba_amount = 0.0

                # note di carico pagate
                # domain = [
                #     ('partner_id', '=', record.id),
                #     ('amount_paid', '>', 0)
                # ]
                # shopping_orders = record.env['sale.order'].search(domain)
                # for order in shopping_orders:
                #     orders_amount += order.amount_total

                # sql = f"""SELECT amount_total
                # FROM sale_order
                # WHERE
                #     partner_id = {record.id} AND
                #     amount_paid > 0
                # """
                # self.env.cr.execute(sql)
                # res = self.env.cr.dictfetchall()
                # if res:
                #     orders_amount += sum(order['amount_total'] for order in res)

                sql = f"""SELECT ol.invoice_status, o.partner_id, ol.price_total, o.state, o.id, o."type" 
                    FROM sale_order_line AS ol
                    LEFT JOIN sale_order AS o 
                    ON o.id = ol.order_id 
                    WHERE 
                    ol.invoice_status != 'invoiced' 
                    AND o.state in ('sale', 'done')
                    AND o.partner_id = {record.id} 
                """
                self.env.cr.execute(sql)
                res = self.env.cr.dictfetchall()
                if res:
                    orders_amount += sum(order['price_total'] for order in res)

                # resi ?
                # domain = [
                #     ('partner_id', '=', record.id),
                #     ('returned_by', '=', True),
                #     ('credit_note', '!=', False)
                # ]
                # # domain.append(('invoice_ids', '=', False)) # ??
                # pickings = record.env['stock.picking'].search(domain)
                # for picking in pickings:
                #     credit_note = picking.credit_note
                #     orders_amount -= credit_note.amount_total

                sql = f"""SELECT cn.amount_total as amount_total
                FROM stock_picking AS sp
                    LEFT JOIN account_invoice as cn
                    ON sp.credit_note = cn.id
                WHERE
                    sp.partner_id = {record.id} AND
                    sp.returned_by = true AND
                    sp.credit_note IS NOT NULL
                """
                self.env.cr.execute(sql)
                orders_amount -= sum(line['amount_total'] for line in self.env.cr.dictfetchall())

                # fatture in bozza and note di credito in bozza
                # domain = [
                #     ('partner_id', '=', record.id),
                #     ('type', 'in', ('out_invoice', 'out_refund')),
                #     ('state', '=', 'draft')
                # ]
                # for invoice in record.env['account.invoice'].search(domain):
                #     if invoice.type == 'out_invoice':
                #         draft_invoices_amount += invoice.amount_total
                #     else:
                #         # 'out_refund'
                #         draft_invoices_amount -= invoice.amount_total

                sql = f"""SELECT amount_total, type
                FROM account_invoice
                WHERE
                    partner_id = {record.id} AND
                    type in ('out_invoice', 'out_refund') AND
                    state = 'draft'
                """
                self.env.cr.execute(sql)
                for invoice in self.env.cr.dictfetchall():
                    if invoice['type'] == 'out_invoice':
                        draft_invoices_amount += invoice['amount_total']
                    else:
                        # 'out_refund'
                        draft_invoices_amount -= invoice['amount_total']

                # # note di credito in bozza
                # domain = list()
                # domain.append(('partner_id', '=', record.id))
                # domain.append(('type', '=', 'out_refund'))
                # domain.append(('state', '=', 'draft'))
                # draft_refound_invoices_ids = record.env['account.invoice'].search(domain)
                #
                # for invoice in draft_refound_invoices_ids:
                #     draft_invoices_amount -= invoice.amount_total

                # riba
                filter_date = (datetime.now() - timedelta(days=2)).strftime(DEFAULT_SERVER_DATE_FORMAT)
                # domain = [
                #     ('partner_id', '=', record.id),
                #     ('reconciled', '=', True),
                #     ('payment_method.code', '=', 'riba_cbi'),
                #     ('date_maturity', '>', filter_date)
                # ]
                # aml_riba = record.env['account.move.line'].search(domain)
                # for line in aml_riba:
                #     riba_amount += line.balance

                sql = f"""SELECT aml.balance as balance
                FROM account_move_line AS aml
                    LEFT JOIN account_payment_method AS apm
                    ON aml.payment_method = apm.id
                WHERE
                    aml.partner_id = {record.id} AND
                    aml.reconciled = true AND
                    apm.code IS NOT NULL AND
                    apm.code = 'riba_cbi' AND
                    aml.date_maturity > '{filter_date}'
                """
                self.env.cr.execute(sql)
                riba_amount += sum(line['balance'] for line in self.env.cr.dictfetchall())

                record.fido_utilizzato = record.credit + draft_invoices_amount + orders_amount + riba_amount
                record.fido_residuo = record.credit_limit - record.fido_utilizzato
                record.esposizione_sbf = riba_amount
                record.fatture_draft = draft_invoices_amount
                record.saldo_contabile = record.debit - record.credit

    def _compute_ddt_to_invoice(self):
        for record in self:
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
            record.ddt_to_invoice = approved_pos_amount

    def _compute_overdue_credit(self):
        current_date = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
        for partner in self:
            sql = """SELECT
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
                                       account_move_line.reconciled = 'false' AND
                                       account_move_line.partner_id = {partner} AND
                                       (account_move_line.date_maturity <= '{data}' 
                                           OR
                                       account_move_line.date <= '{data}' AND account_move_line.date_maturity IS NULL)
                                   GROUP BY
                                       account_move_line.partner_id;
                                    
                               """.format(partner=partner.id, data=current_date)
            self.env.cr.execute(sql)

            res_sql = self.env.cr.fetchall()

            for res_id in res_sql:
                partner.overdue_credit = res_id[1]

    fido_utilizzato = fields.Float(
        string='Fido utilizzato',
        compute='_compute_fido',
        help="Credito + Fatture Draft + Ordini + RiBa"
    )

    fido_residuo = fields.Float(
        string='Fido residuo',
        compute='_compute_fido',
    )

    saldo_contabile = fields.Float(
        string='Saldo Contabile',
        compute='_compute_fido',
    )

    fatture_draft = fields.Float(
        string='Fatture da Registrare',
        compute='_compute_fido',
    )

    esposizione_sbf = fields.Float(
        string='Esposizione SBF',
        compute='_compute_fido',
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
        compute=_compute_ddt_to_invoice,
    )

    overdue_credit = fields.Float(
        string='Totale Scaduto',
        compute='_compute_overdue_credit',
        search='_search_overdue_credit',
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
