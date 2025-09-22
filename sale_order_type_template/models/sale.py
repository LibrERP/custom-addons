# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models


class SaleOrderType(models.Model):
    _inherit = "sale.order.type"

    sale_order_template_id = fields.Many2one(
        comodel_name='sale.order.template',
        string='Quotation Template Reference',
        index=True,
        ondelete='cascade'
    )


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange('type_id')
    def _onchange_type_id(self):
        self.ensure_one()

        if self.type_id and self.type_id.sale_order_template_id:
            self.sale_order_template_id = self.type_id.sale_order_template_id.id
