# Copyright 2023 Didotech s.r.l. <https://www.didotech.com>
#
from odoo import models, fields, api


class DueDateManager(models.Model):
    _inherit = 'account.duedate_plus.manager'
    _description = 'Gestore scadenze fatture/note di credito'

    @api.model
    def _set_amount_total(self, types, amount):
        if self.invoice_id and self.invoice_id.has_deposit:
            amount -= self.invoice_id.deposit
        return super()._set_amount_total(types, amount)

    @api.model
    def _validate_duedates_amount(self):
        """
        Enforces the following constraint:

        the sum of the amount of each the duedate related to this account.move
        must be equal to the account.move amount
        """
        res = super()._validate_duedates_amount()

        if res is not None:
            # verify
            if self.invoice_id.has_deposit:
                precision = self.invoice_id.currency_id.decimal_places
                total = self.invoice_id.deposit + self.invoice_id.amount_net_pay
                if self.invoice_id.amount_total == total:
                    return None

        return res

    # end _validate_duedates_amount

    @api.model
    def _extra_line(self, inv_date, payment_method_id, types):
        row = {}
        row = super().__extra_line(inv_date, payment_method_id, types)
        if types['deposit']:
            row['due_amount'] = self.invoice_id.deposit
            row['duedate_manager_id'] = self.id
            row['due_date'] = inv_date
            row['payment_method_id'] = payment_method_id

        return row

    # end _extra_lines

    @api.model
    def _extra_duedate_line(self, param_cm, types_amount, payment_method_id):
        line = {}
        line = super()._extra_duedate_line(param_cm, types_amount, payment_method_id)
        split_date = self._get_split_date_period(
            param_cm['partner_id'],
            param_cm['doc_type'],
            param_cm['invoice_date'].strftime('%Y-%m-%d'),
        )
        if 'deposit' in types_amount and bool(types_amount['deposit']):
            line['duedate_manager_id'] = self.id
            line['due_amount'] = self.invoice_id.deposit
            line['due_date'] = split_date
            line['payment_method_id'] = payment_method_id
        # end if

        return line

    @api.model
    def _get_amount_tax_type(self):
        typess = super()._get_amount_tax_type()
        if self.invoice_id and self.invoice_id.has_deposit:
            typess['deposit'] = self.invoice_id.deposit
        return typess
    # end _get_amount_tax_type

    @api.model
    def _get_tax_type(self):
        typess = super()._get_tax_type()
        if self.invoice_id and self.invoice_id.has_deposit:
            typess['is_deposit'] = self.invoice_id.deposit
        return typess
    # end _get_amount_tax_type


