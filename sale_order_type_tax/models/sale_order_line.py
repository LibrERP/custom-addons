# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange('product_id')
    def _onchange_product_id_set_tax(self):
        if not self.product_id:
            return

        if self.order_id.type_id.tax_id:
            self.tax_id = [Command.link(self.order_id.type_id.tax_id.id)]
