# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ContractRecurringMixin(models.AbstractModel):
    _inherit = "contract.recurring.mixin"

    @api.constrains("recurring_interval", "date_end")
    def _check_recurring_interval(self):
        # A zero (or negative) interval makes the billing period zero-length:
        # recurring_next_date never advances, so the generation cron keeps
        # finding the contract "due" and regenerates a document every day.
        # Finished contracts (date_end in the past) no longer generate, so a
        # zero interval is harmless there and must stay editable/archivable.
        today = fields.Date.context_today(self)
        for record in self:
            if record.recurring_interval is False or record.recurring_interval > 0:
                continue
            if record.date_end and record.date_end < today:
                continue
            raise ValidationError(
                self.env._(
                    "The recurrence interval (\"Invoice Every\") must be "
                    "greater than zero."
                )
            )
