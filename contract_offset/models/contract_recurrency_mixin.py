# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class ContractRecurrencyBasicMixin(models.AbstractModel):
    _inherit = "contract.recurrency.basic.mixin"

    recurring_invoicing_offset = fields.Integer(
        compute="_compute_recurring_invoicing_offset",
        store=True,
        readonly=False,
        copy=True,
        help=(
            "Positive (>=1): day N within the relevant period.\n"
            "  - pre-paid: day N of the current period.\n"
            "  - post-paid: day N of the next period (the one after the "
            "service period).\n"
            "Negative (<=-1): N days before the start of the period after "
            "the anchor period.\n"
            "  - pre-paid: anchor = next_period_start.\n"
            "  - post-paid: anchor = period_after_next_start."
        ),
    )


class ContractRecurrencyMixin(models.AbstractModel):
    _inherit = "contract.recurrency.mixin"

    recurring_next_date = fields.Date(
        compute="_compute_recurring_next_date",
        inverse="_inverse_recurring_next_date",
        store=True,
        readonly=False,
        copy=True,
    )

    @api.model
    def _contract_offset_anchors(
        self,
        next_period_date_start,
        recurring_invoicing_type,
        recurring_rule_type,
        recurring_interval,
    ):
        """Return (positive_anchor, negative_anchor) for the offset formula.

        Pre-paid: positive = period_start, negative = next_period_start.
        Post-paid: each shifted one delta forward.
        """
        delta = self.get_relative_delta(recurring_rule_type, recurring_interval)
        if recurring_invoicing_type == "post-paid":
            positive_anchor = next_period_date_start + delta
            negative_anchor = next_period_date_start + delta + delta
        else:  # pre-paid (default)
            positive_anchor = next_period_date_start
            negative_anchor = next_period_date_start + delta
        return positive_anchor, negative_anchor

    @api.model
    def get_next_invoice_date(
        self,
        next_period_date_start,
        recurring_invoicing_type,
        recurring_invoicing_offset,
        recurring_rule_type,
        recurring_interval,
        max_date_end,
    ):
        if not next_period_date_start:
            return False
        positive_anchor, negative_anchor = self._contract_offset_anchors(
            next_period_date_start,
            recurring_invoicing_type,
            recurring_rule_type,
            recurring_interval,
        )
        if recurring_invoicing_offset > 0:
            rnd = positive_anchor + relativedelta(
                days=recurring_invoicing_offset - 1
            )
        elif recurring_invoicing_offset < 0:
            rnd = negative_anchor + relativedelta(
                days=recurring_invoicing_offset
            )
        else:
            rnd = positive_anchor
        if max_date_end and rnd > max_date_end:
            return False
        return rnd

    @api.depends(
        "last_date_invoiced",
        "date_start",
        "date_end",
        "recurring_rule_type",
        "recurring_interval",
    )
    def _compute_next_period_date_start(self):
        """Walk the recurrence sequence from date_start; pick the first
        period_start that comes after last_date_invoiced."""
        for rec in self:
            if not rec.date_start:
                rec.next_period_date_start = False
                continue
            period_start = rec.date_start
            if rec.last_date_invoiced:
                delta = rec.get_relative_delta(
                    rec.recurring_rule_type, rec.recurring_interval
                )
                # Safety bound to avoid runaway loops on bad data.
                for _ in range(10000):
                    if period_start > rec.last_date_invoiced:
                        break
                    period_start = period_start + delta
            if rec.date_end and period_start > rec.date_end:
                rec.next_period_date_start = False
            else:
                rec.next_period_date_start = period_start

    @api.depends(
        "next_period_date_start",
        "recurring_rule_type",
        "recurring_interval",
        "date_end",
    )
    def _compute_next_period_date_end(self):
        """period_end = period_start + delta - 1, clamped to date_end."""
        for rec in self:
            rec.next_period_date_end = self.get_next_period_date_end(
                rec.next_period_date_start,
                rec.recurring_rule_type,
                rec.recurring_interval,
                max_date_end=rec.date_end,
            )

    @api.depends(
        "next_period_date_start",
        "recurring_invoicing_offset",
        "recurring_invoicing_type",
        "recurring_rule_type",
        "recurring_interval",
        "date_end",
    )
    def _compute_recurring_next_date(self):
        for rec in self:
            rec.recurring_next_date = self.get_next_invoice_date(
                rec.next_period_date_start,
                rec.recurring_invoicing_type,
                rec.recurring_invoicing_offset,
                rec.recurring_rule_type,
                rec.recurring_interval,
                max_date_end=rec.date_end,
            )

    def _derive_offset_from_recurring_next_date(self):
        """Shared helper: derive offset from current recurring_next_date,
        preserving the sign of the existing offset."""
        self.ensure_one()
        if not (self.recurring_next_date and self.next_period_date_start):
            return
        positive_anchor, negative_anchor = self._contract_offset_anchors(
            self.next_period_date_start,
            self.recurring_invoicing_type,
            self.recurring_rule_type,
            self.recurring_interval,
        )
        if self.recurring_invoicing_offset >= 0:
            days = (self.recurring_next_date - positive_anchor).days
            new_offset = days + 1 if days >= 0 else days
        else:
            new_offset = (self.recurring_next_date - negative_anchor).days
        if self.recurring_invoicing_offset != new_offset:
            self.recurring_invoicing_offset = new_offset

    def _inverse_recurring_next_date(self):
        """Fires on actual write/save."""
        for rec in self:
            rec._derive_offset_from_recurring_next_date()

    @api.onchange("recurring_next_date")
    def _onchange_recurring_next_date(self):
        """Fires live in the form when the user types a new date, so the
        offset display updates immediately."""
        for rec in self:
            rec._derive_offset_from_recurring_next_date()