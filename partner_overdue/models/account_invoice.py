
from odoo import models, fields, api, tools, _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    _description = "Invoice with index on partner"

    @api.model_cr_context
    def _auto_init(self):
        res = super()._auto_init()
        tools.create_index(self._cr, 'account_invoice_partner_id_idx',
                           self._table, ['partner_id'])
        return res

