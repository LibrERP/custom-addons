# © 2022 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ResCompany(models.Model):
    _inherit = 'res.company'

    def get_purchase_journal(self):
        journal_model = self.env['account.journal']
        journals = journal_model.search(
            [
                ('type', '=', 'purchase'),
                ('company_id', '=', self.id)
            ],
            limit=1)
        if not journals:
            raise UserError(
                _(
                    "Define a purchase journal "
                    "for this company: '%s' (id: %d)."
                ) % (self.name, self.id)
            )
        return journals[0]
