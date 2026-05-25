# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models
from odoo.tools.misc import clean_context


class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    def _do_create_moves(self):
        """
        Block own account sheets from move creation
        """
        self = self.with_context(clean_context(self.env.context))  # remove default_*
        own_account_sheets = self.filtered(lambda sheet: sheet.payment_mode == 'own_account')
        company_account_sheets = self - own_account_sheets

        return super(HrExpenseSheet, company_account_sheets)._do_create_moves()
