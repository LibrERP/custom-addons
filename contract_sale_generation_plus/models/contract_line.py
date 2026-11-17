# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class ContractLine(models.Model):
    _inherit = "contract.line"

    def _prepare_sale_line_vals(self, dates, order_id=False):
        sale_line_vals = super()._prepare_sale_line_vals(dates, order_id)

        sale_line_vals['analytic_distribution'] = self.analytic_distribution

        if self.product_id.must_have_dates:
            # dates = _get_period_to_invoice(...) = (period_start, period_end,
            # recurring_next_date); dates[1] is the correct invoice period end
            # (it accounts for recurring_invoicing_type/offset). A valid period
            # requires recurring_interval > 0, which is enforced by the
            # _check_recurring_interval constraint on contract.recurring.mixin.
            sale_line_vals.update({
                'start_date': dates[0],
                'end_date': dates[1],
            })

        return sale_line_vals
