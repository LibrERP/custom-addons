# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    def _aggregate_by_tax(self, lines):
        values_per_grouping_key = {}

        for line in lines:
            for tax in line['tax_details']['taxes_data']:
                if tax['tax'].id in values_per_grouping_key:
                    values_per_grouping_key[tax['tax'].id]['tax_amount_currency'] += tax['tax_amount_currency']
                    values_per_grouping_key[tax['tax'].id]['tax_amount'] += tax['tax_amount']
                    values_per_grouping_key[tax['tax'].id]['base_amount_currency'] += tax['base_amount_currency']
                    values_per_grouping_key[tax['tax'].id]['base_amount'] += tax['base_amount']
                    values_per_grouping_key[tax['tax'].id]['display_base_amount_currency'] += tax['base_amount_currency']
                    values_per_grouping_key[tax['tax'].id]['display_base_amount'] += tax['base_amount']
                else:
                    values_per_grouping_key[tax['tax'].id] = {
                        'id': tax['tax'].id,
                        # 'involved_tax_ids': involved_taxes.ids,
                        'tax_amount_currency': tax['tax_amount_currency'],
                        'tax_amount': tax['tax_amount'],
                        'base_amount_currency': tax['base_amount_currency'],
                        'base_amount': tax['base_amount'],
                        'display_base_amount_currency': tax['base_amount_currency'],
                        'display_base_amount': tax['base_amount'],
                        'group_name': tax['tax'].invoice_label or tax['tax'].name,
                        'group_label': tax['tax'].name
                    }

        return list(values_per_grouping_key.values())

    @api.model
    def _get_tax_totals_summary(self, base_lines, currency, company, cash_rounding=None):
        summary = super()._get_tax_totals_summary(base_lines, currency, company, cash_rounding=cash_rounding)

        summary['subtotals'][0]['tax_grouped_by_tax'] = self._aggregate_by_tax(base_lines)

        return summary
