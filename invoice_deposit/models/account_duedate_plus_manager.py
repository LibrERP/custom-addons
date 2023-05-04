# Copyright 2023 Didotech s.r.l. <https://www.didotech.com>
#
from odoo import models, fields, api


class DueDateManager(models.Model):
    _inherit = 'account.duedate_plus.manager'
    _description = 'Gestore scadenze fatture/note di credito'

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

