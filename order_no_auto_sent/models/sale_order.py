# © 2022 Didotech srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models, api, fields, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def print_quotation(self):
        # Draft orders remains in draft
        draft_orders = self.filtered(lambda s: s.state == 'draft')
        result = super().print_quotation()
        draft_orders.write({'state': 'draft'})
        return result
