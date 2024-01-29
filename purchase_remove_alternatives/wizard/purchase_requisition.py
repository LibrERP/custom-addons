# © 2023 Andrei Levin <andrei.levin@didotech.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
from odoo import api, fields, models


class PurchaseRequisitionAlternativeWarning(models.TransientModel):
    _inherit = 'purchase.requisition.alternative.warning'

    def action_remove_alternatives(self):
        # Remove discarded lines
        self.po_ids.mapped('order_line').filtered(lambda ol: ol.product_qty == 0).unlink()
        self.alternative_po_ids.mapped('order_line').filtered(lambda ol: ol.product_qty == 0).unlink()

        for line in self.po_ids.mapped('order_line'):
            for alternative_po in self.alternative_po_ids:
                condemned_lines = alternative_po.mapped('order_line').filtered(
                    lambda ol: ol.product_qty == line.product_qty and ol.product_id.id == line.product_id.id
                )
                if condemned_lines:
                    condemned_lines[0].unlink()

        self.alternative_po_ids.filtered(
            lambda po: not len(po.order_line)
        ).filtered(
            lambda po: po.state in ['draft', 'sent', 'to approve'] and po.id not in self.po_ids.ids
        ).button_cancel()
        return self._action_done()