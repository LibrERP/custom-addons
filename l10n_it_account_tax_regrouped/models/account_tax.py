# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    def _aggregate_by_tax(self, lines):
        values_per_grouping_key = {}

        for line in lines:
            if line['tax_ids'].id in values_per_grouping_key:
                values_per_grouping_key[line['tax_ids'].id]['tax_amount_currency'] += line['tax_details']['raw_total_included_currency'] - line['tax_details']['raw_total_excluded_currency']
                values_per_grouping_key[line['tax_ids'].id]['tax_amount'] += line['tax_details']['raw_total_included'] - line['tax_details']['raw_total_excluded']
                values_per_grouping_key[line['tax_ids'].id]['base_amount_currency'] += line['tax_details']['total_excluded_currency']
                values_per_grouping_key[line['tax_ids'].id]['base_amount'] += line['tax_details']['total_excluded']
                values_per_grouping_key[line['tax_ids'].id]['display_base_amount_currency'] += line['tax_details']['total_excluded_currency']
                values_per_grouping_key[line['tax_ids'].id]['display_base_amount'] += line['tax_details']['total_excluded']
            else:
                values_per_grouping_key[line['tax_ids'].id] = {
                    'id': line['tax_ids'].id,
                    # 'involved_tax_ids': involved_taxes.ids,
                    'tax_amount_currency': line['tax_details']['raw_total_included_currency'] - line['tax_details']['raw_total_excluded_currency'],
                    'tax_amount': line['tax_details']['raw_total_included'] - line['tax_details']['raw_total_excluded'],
                    'base_amount_currency': line['tax_details']['total_excluded_currency'],
                    'base_amount': line['tax_details']['total_excluded'],
                    'display_base_amount_currency': line['tax_details']['total_excluded_currency'],
                    'display_base_amount': line['tax_details']['total_excluded'],
                    'group_name': line['tax_ids'].name,
                    'group_label': line['tax_ids'].name
                }

        return list(values_per_grouping_key.values())

    @api.model
    def _get_tax_totals_summary(self, base_lines, currency, company, cash_rounding=None):
        summary = super()._get_tax_totals_summary(base_lines, currency, company, cash_rounding=cash_rounding)

        summary['subtotals'][0]['tax_grouped_by_tax'] = self._aggregate_by_tax(base_lines)

        return summary
