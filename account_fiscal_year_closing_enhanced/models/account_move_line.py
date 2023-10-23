# Copyright 2023 Fabio Giovannelli Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#

from odoo import api, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.multi
    def check_partner(self):
        res = super().check_partner()
        # check only if super return false
        if res:
            return res
        journal_ids = self.get_fiscal_year_closing_journals()

        types = self.env["account.account.type"].search(
            [("type", "in", ["receivable", "payable"])]
        )

        if types:
            type_ids = [ty.id for ty in types]
            if self.account_id.user_type_id.id in type_ids and self.journal_id.id not in journal_ids:
                if self.partner_id.id is False:
                    return False

        return True

    def get_fiscal_year_closing_journals(self):
        journals = []
        closing_ids = self.env['account.fiscalyear.closing.template'].search([])
        for closing in closing_ids:
            if closing.move_config_ids:
                journals = closing.move_config_ids.mapped('journal_id').ids
        return journals

