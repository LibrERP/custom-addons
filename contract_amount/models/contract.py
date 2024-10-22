# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import Command, api, fields, models, _, Command


class ContractContract(models.Model):
    _inherit = "contract.contract"

    amount_untaxed = fields.Monetary(string="Total", store=True, compute='_compute_amounts', tracking=4)

    @api.depends('contract_line_ids.price_subtotal', 'contract_line_ids.quantity', 'contract_line_ids.price_unit')
    def _compute_amounts(self):
        for contract in self:
            contract_lines = contract.contract_line_ids.filtered(lambda x: not x.display_type)
            contract.amount_untaxed = sum(contract_lines.mapped('price_subtotal'))
