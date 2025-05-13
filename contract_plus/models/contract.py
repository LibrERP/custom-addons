# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


class ContractContract(models.Model):
    _inherit = "contract.contract"

    def _prepare_recurring_sales_values(self, date_ref=False):
        sales_values = super()._prepare_recurring_sales_values(date_ref=date_ref)

        for sale_values in sales_values:
            for line in sale_values['order_line']:
                if not self.line_is_valid(line[2].get('display_type'), line[2].get('product_id', False), line[2].get('product_uom', False)):
                    message = f"Contract \"{sale_values['origin']}\" contains lines without Product or without UoM"
                    _logger.info(message)
                    raise UserError(message)

        return sales_values

    def line_is_valid(self, display_type, product_id, product_uom):
        """
        "CHECK(display_type IS NOT NULL OR (product_id IS NOT NULL AND product_uom IS NOT NULL))"
        """

        return display_type or (product_id and product_uom)

    def check_sale_values(self):
        self.ensure_one()

        for line in self.contract_line_ids:
            if not self.line_is_valid(line.display_type, line.product_id, line.uom_id):
                message = f"Contract \"{self.name}\" contains line without Product or without UoM: {line.name}"
                _logger.info(message)
                raise UserError(message)

    def write(self, values):
        result = super().write(values)
        for contract in self:
            if contract.generation_type == 'sale':
                contract.check_sale_values()
        return result

    @api.model_create_multi
    def create(self, values):
        contracts = super().create(values=values)
        for contract in contracts:
            if contract.generation_type == 'sale':
                contract.check_sale_values()

        return contracts
