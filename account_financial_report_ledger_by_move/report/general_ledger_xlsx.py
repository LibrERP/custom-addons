
# Author: Damien Crier
# Author: Julien Coux
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, models


class GeneralLedgerXslx(models.AbstractModel):
    _inherit = 'report.a_f_r.report_general_ledger_xlsx'
    # _inherit = 'report.account_financial_report.abstract_report_xlsx'

    def _get_report_name(self, report):
        report_name = _('General Ledger')
        return self._get_report_complete_name(report, report_name)

    # def _get_report_columns(self, report):
    #     res = {
    #         0: {'header': _('Date'), 'field': 'date', 'width': 11},
    #         1: {'header': _('Entry'), 'field': 'entry', 'width': 18},
    #         2: {'header': _('Journal'), 'field': 'journal', 'width': 8},
    #         3: {'header': _('Account'), 'field': 'account', 'width': 9},
    #         4: {'header': _('Taxes'),
    #             'field': 'taxes_description',
    #             'width': 15},
    #         5: {'header': _('Partner'), 'field': 'partner', 'width': 25},
    #         6: {'header': _('Ref - Label'), 'field': 'label', 'width': 40},
    #         7: {'header': _('Cost center'),
    #             'field': 'cost_center',
    #             'width': 15},
    #         8: {'header': _('Tags'),
    #             'field': 'tags',
    #             'width': 10},
    #         9: {'header': _('Rec.'), 'field': 'matching_number', 'width': 5},
    #         10: {'header': _('Debit'),
    #              'field': 'debit',
    #              'field_initial_balance': 'initial_debit',
    #              'field_final_balance': 'final_debit',
    #              'type': 'amount',
    #              'width': 14},
    #         11: {'header': _('Credit'),
    #              'field': 'credit',
    #              'field_initial_balance': 'initial_credit',
    #              'field_final_balance': 'final_credit',
    #              'type': 'amount',
    #              'width': 14},
    #         12: {'header': _('Cumul. Bal.'),
    #              'field': 'cumul_balance',
    #              'field_initial_balance': 'initial_balance',
    #              'field_final_balance': 'final_balance',
    #              'type': 'amount',
    #              'width': 14},
    #     }
    #     if report.foreign_currency:
    #         foreign_currency = {
    #             13: {'header': _('Cur.'),
    #                  'field': 'currency_id',
    #                  'field_currency_balance': 'currency_id',
    #                  'type': 'many2one', 'width': 7},
    #             14: {'header': _('Amount cur.'),
    #                  'field': 'amount_currency',
    #                  'field_initial_balance':
    #                      'initial_balance_foreign_currency',
    #                  'field_final_balance':
    #                      'final_balance_foreign_currency',
    #                  'type': 'amount_currency',
    #                  'width': 14},
    #         }
    #         res = {**res, **foreign_currency}
    #     return res

    def _get_report_filters(self, report):
        res = super()._get_report_filters(report)
        group_by = [
                _('Raggruppato per Registrazione'),
                _('Yes') if report.group_by_move else _('No')
            ]
        res.append(group_by)
        return res

    # def _get_col_count_filter_name(self):
    #     return 2
    #
    # def _get_col_count_filter_value(self):
    #     return 2
    #
    # def _get_col_pos_initial_balance_label(self):
    #     return 5
    #
    # def _get_col_count_final_balance_name(self):
    #     return 5
    #
    # def _get_col_pos_final_balance_label(self):
    #     return 5

    def _generate_report_content(self, workbook, report):
        # For each account
        for account in report.account_ids:
            # Write account title
            self.write_array_title(account.code + ' - ' + account.name)

            if not account.partner_ids:
                # Display array header for move lines
                self.write_array_header()

                # Display initial balance line for account
                self.write_initial_balance(account)

                if report.group_by_move:
                    for line in account.move_ids:
                        self.write_line(line)
                else:
                    # Display account move lines
                    for line in account.move_line_ids:
                        self.write_line(line)

            else:
                # For each partner
                for partner in account.partner_ids:
                    # Write partner title
                    self.write_array_title(partner.name)

                    # Display array header for move lines
                    self.write_array_header()

                    # Display initial balance line for partner
                    self.write_initial_balance(partner)

                    if report.group_by_move:
                        # Display account move lines
                        for line in partner.move_ids:
                            self.write_line(line)
                    else:
                        for line in partner.move_line_ids:
                            self.write_line(line)

                    # Display ending balance line for partner
                    self.write_ending_balance(partner)

                    # Line break
                    self.row_pos += 1

            # Display ending balance line for account
            if not report.filter_partner_ids:
                self.write_ending_balance(account)

            # 2 lines break
            self.row_pos += 2

    # def write_initial_balance(self, my_object):
    #     """Specific function to write initial balance for General Ledger"""
    #     if 'partner' in my_object._name:
    #         label = _('Partner Initial balance')
    #         my_object.currency_id = my_object.report_account_id.currency_id
    #     elif 'account' in my_object._name:
    #         label = _('Initial balance')
    #     super(GeneralLedgerXslx, self).write_initial_balance(
    #         my_object, label
    #     )
    #
    # def write_ending_balance(self, my_object):
    #     """Specific function to write ending balance for General Ledger"""
    #     if 'partner' in my_object._name:
    #         name = my_object.name
    #         label = _('Partner ending balance')
    #     elif 'account' in my_object._name:
    #         name = my_object.code + ' - ' + my_object.name
    #         label = _('Ending balance')
    #     super(GeneralLedgerXslx, self).write_ending_balance(
    #         my_object, name, label
    #     )
