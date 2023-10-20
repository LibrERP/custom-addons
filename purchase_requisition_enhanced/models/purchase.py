# © 2023 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models, _, Command


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    allocated = fields.Boolean(default=False)

    def action_choose(self):
        self = self.order_id.order_line.filtered(lambda l: l.product_id.id == self.product_id.id)
        self.write({'allocated': True})
        # We should explicitly pass 'self' to super() if not sometime initial value will be used
        return super(PurchaseOrderLine, self).action_choose()
