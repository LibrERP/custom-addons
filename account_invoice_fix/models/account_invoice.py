# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.model
    def _get_refund_common_fields(self):
        fields = super()._get_refund_common_fields()
        fields.append('user_id')

        return fields
