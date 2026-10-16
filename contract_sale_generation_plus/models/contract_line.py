# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class ContractLine(models.Model):
    _inherit = "contract.line"

    def _prepare_sale_line_vals(self, dates, order_id=False):
        sale_line_vals = super()._prepare_sale_line_vals(dates, order_id)

        sale_line_vals['analytic_distribution'] = self.analytic_distribution
        return sale_line_vals
