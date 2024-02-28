# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from collections import defaultdict
from datetime import timedelta

from odoo import api, fields, models, _
# from odoo.exceptions import ValidationError
# from odoo.osv.expression import AND


class CrossoveredBudgetLines(models.Model):
    _inherit = "crossovered.budget.lines"

    expected_amount = fields.Monetary(
        compute='_compute_forecast_amount', string='Expected Amount', help="Amount that should be earned/spent.")

    def _compute_forecast_amount(self):
        for line in self:
            sale_domain = [
                ('state', 'in', ('sale', 'done')),
                ('order_id.date_order', '>=', line.date_from),
                ('order_id.date_order', '<=', line.date_to)
            ]
            purchase_domain = [
                ('state', 'in', ('purchase', 'done')),
                ('order_id.date_order', '>=', line.date_from),
                ('order_id.date_order', '<=', line.date_to)
            ]
            if line.analytic_account_id:
                analytic_account = line.analytic_account_id
                # TODO: take in consideration analytic_distribution
                sale_domain.append(
                    ('order_id.analytic_account_id', '=', analytic_account.id),

                )
                purchase_domain.append(
                    ('project_id.analytic_account_id', '=', analytic_account.id)
                )

            if line.general_budget_id:
                accounts = line.general_budget_id.account_ids
                sale_domain += [
                    '|',
                    ('product_id.property_account_income_id', 'in', accounts.ids),
                    ('product_id.categ_id.property_account_income_categ_id', 'in', accounts.ids)
                ]
                purchase_domain += [
                    '|',
                    ('product_id.property_account_expense_id', 'in', accounts.ids),
                    ('product_id.categ_id.property_account_expense_categ_id', 'in', accounts.ids)
                ]

            sale_order_lines = self.env['sale.order.line'].search(sale_domain)
            purchase_order_lines = self.env['purchase.order.line'].search(purchase_domain)

            if sale_order_lines or purchase_order_lines:
                line.expected_amount = sum(sale_order_lines.mapped('price_subtotal')) - sum(purchase_order_lines.mapped('price_subtotal'))
            else:
                line.expected_amount = 0.0
