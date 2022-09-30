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
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime, timedelta


class PosOrderInvoiceGroup(models.Model):
    _name = 'pos.order.invoice.group'
    _description = 'Scadenziario mensile'
    _rec_name = 'partner_id'
    _order = "year_amount desc, year desc"
    _auto = False

    position = fields.Integer('Posizione')
    partner_id = fields.Many2one('res.partner', 'Partner', SELECT=1, ondelete='restrict')
    property_customer_ref = fields.Char('Codice Cliente', size=16)
    year = fields.Char('Anno')
    jan = fields.Float('Gen')
    feb = fields.Float('Feb')
    mar = fields.Float('Mar')
    apr = fields.Float('Apr')
    may = fields.Float('Mag')
    jun = fields.Float('Giu')
    jul = fields.Float('Lug')
    aug = fields.Float('Ago')
    sep = fields.Float('Set')
    oct = fields.Float('Ott')
    nov = fields.Float('Nov')
    dec = fields.Float('Dic')
    year_amount = fields.Float('Somma')
    total_years = fields.Float('Totale Anno')
    ratio = fields.Float(u'% Fatturato')
    cumulative_sales = fields.Float('Cumulativo')
    pareto = fields.Boolean(u'> 80% fatturato')
    overdue = fields.Float(string="Overdue Payment")

    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'pos_order_invoice_group_month')
        tools.drop_view_if_exists(self.env.cr, 'partner_overdue_credit')
        tools.drop_view_if_exists(self.env.cr, 'pos_order_invoice_group')

        self.env.cr.execute("""
            CREATE or REPLACE view pos_order_invoice_group_month AS (
            SELECT
                min(invoice.id) AS id,
                invoice.partner_id AS partner_id,
                to_char(invoice.date_invoice, 'YYYY'::text) AS year,
                to_char(invoice.date_invoice, 'MM'::text) AS month,
                SUM(
                    CASE
                        WHEN type = 'out_invoice' THEN invoice.amount_untaxed
                    ELSE -invoice.amount_untaxed
                    END
                ) AS amount_untaxed
                FROM account_invoice AS invoice
                WHERE invoice.type IN ('out_invoice', 'out_refund') AND invoice.state NOT IN ('draft', 'cancel') AND partner_id != 1
                GROUP BY (to_char(invoice.date_invoice, 'YYYY'::text)), (to_char(invoice.date_invoice, 'MM'::text)), invoice.partner_id ORDER BY year desc
            );
            
            CREATE or REPLACE view partner_overdue_credit AS (
                SELECT
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
                       (account_move_line.date_maturity <= now()::DATE 
                           OR
                       account_move_line.date <= now()::DATE AND account_move_line.date_maturity IS NULL)
    
                   GROUP BY
                       account_move_line.partner_id
            );

            CREATE or REPLACE view pos_order_invoice_group AS (
                SELECT
                    row_number() OVER (PARTITION BY A.year ORDER BY A.year desc, A.year_amount desc) AS position,
                    A.id, 
                    A.partner_id, 
                    C.property_customer_ref,
                    A.year, 
                    A.jan, A.feb, A.mar, A.apr, A.may, A.jun, A.jul, A.aug, A.sep, A.oct, A.nov, A.dec, 
                    A.year_amount, 
                    B.amount_untaxed AS total_years,
                    (100 * A.year_amount / B.amount_untaxed) AS ratio,
                    sum(A.year_amount) OVER (ORDER BY A.year desc, A.year_amount desc rows unbounded preceding) as cumulative_sales,
                    CASE
                        WHEN sum(A.year_amount) OVER (PARTITION BY A.year ORDER BY A.year desc, A.year_amount desc rows unbounded preceding) < 0.8 * B.amount_untaxed THEN True
                        ELSE Null
                    END as pareto,
                    COALESCE(D.overdue, 0.0) AS overdue


                    FROM 
                    (SELECT min(id) AS id, 
                                    partner_id AS partner_id, 
                                    year AS year, 
                                    (SELECT amount_untaxed from pos_order_invoice_group_month where "month" = '01' AND partner_id=p.partner_id AND year=p.year) AS jan,
                                    (SELECT amount_untaxed from pos_order_invoice_group_month where "month" = '02' AND partner_id=p.partner_id AND year=p.year) AS feb,
                                    (SELECT amount_untaxed from pos_order_invoice_group_month where "month" = '03' AND partner_id=p.partner_id AND year=p.year) AS mar,
                                    (SELECT amount_untaxed from pos_order_invoice_group_month where "month" = '04' AND partner_id=p.partner_id AND year=p.year) AS apr,
                                    (SELECT amount_untaxed from pos_order_invoice_group_month where "month" = '05' AND partner_id=p.partner_id AND year=p.year) AS may,
                                    (SELECT amount_untaxed from pos_order_invoice_group_month where "month" = '06' AND partner_id=p.partner_id AND year=p.year) AS jun,
                                    (SELECT amount_untaxed from pos_order_invoice_group_month where "month" = '07' AND partner_id=p.partner_id AND year=p.year) AS jul,
                                    (SELECT amount_untaxed from pos_order_invoice_group_month where "month" = '08' AND partner_id=p.partner_id AND year=p.year) AS aug,
                                    (SELECT amount_untaxed from pos_order_invoice_group_month where "month" = '09' AND partner_id=p.partner_id AND year=p.year) AS sep,
                                    (SELECT amount_untaxed from pos_order_invoice_group_month where "month" = '10' AND partner_id=p.partner_id AND year=p.year) AS oct,
                                    (SELECT amount_untaxed from pos_order_invoice_group_month where "month" = '11' AND partner_id=p.partner_id AND year=p.year) AS nov,
                                    (SELECT amount_untaxed from pos_order_invoice_group_month where "month" = '12' AND partner_id=p.partner_id AND year=p.year) AS dec,
                                    (SELECT sum(amount_untaxed) from pos_order_invoice_group_month where partner_id=p.partner_id AND year=p.year) AS year_amount
                                FROM pos_order_invoice_group_month p 
                                GROUP BY partner_id, year ORDER BY year_amount desc) as A,
                    (SELECT sum(amount_untaxed) AS amount_untaxed, year FROM pos_order_invoice_group_month GROUP BY year) as B,
                    res_partner as C
                    LEFT JOIN partner_overdue_credit D ON
                    D.partner_id = C.id 

                WHERE A.year=B.year AND A.partner_id = C.id ORDER BY A.year desc, A.year_amount desc)""")
