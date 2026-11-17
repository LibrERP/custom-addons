# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    contract_ids = fields.One2many(comodel_name='contract.contract', compute='_compute_contract_ids')

    @api.depends('order_line.contract_line_id.contract_id')
    def _compute_contract_ids(self):
        for order in self:
            contract_ids = order.order_line.mapped('contract_line_id').mapped('contract_id')
            if contract_ids:
                order.contract_ids = [Command.set(contract_ids.ids)]
            else:
                order.contract_ids = False
