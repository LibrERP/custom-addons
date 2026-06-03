# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ContractRecurrencyBasicMixin(models.AbstractModel):
    _inherit = "contract.recurrency.basic.mixin"

    recurring_invoicing_offset = fields.Integer(
        compute="_compute_recurring_invoicing_offset",
        store=True,
        readonly=False,
        copy=True,
        help=(
            "Pre-paid (offset counted from the service period start):\n"
            "  - N >= 1: day N within the service period "
            "(rnd = period_start + N - 1).\n"
            "  - N = 0: invoice on period_start (same as offset 1).\n"
            "  - N <= -1: N days before period_start "
            "(rnd = period_start + N; offset -1 is the day before "
            "the period starts).\n"
            "Post-paid (offset counted from the service period end):\n"
            "  - N >= 1: rnd = period_end + N (N days after period_end).\n"
            "  - N = 0: rnd = period_end + 1 (the day after the period "
            "ends; same as offset 1).\n"
            "  - N <= -1: rnd = period_end + N + 1 (offset -1 invoices "
            "on the last day of the period; offset -2 invoices one day "
            "before period_end, etc.)."
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
        if recurring_invoicing_type == "post-paid":
            delta = self.get_relative_delta(
                recurring_rule_type, recurring_interval
            )
            period_end = (
                next_period_date_start + delta - relativedelta(days=1)
            )
            if recurring_invoicing_offset > 0:
                rnd = period_end + relativedelta(
                    days=recurring_invoicing_offset
                )
            else:
                rnd = period_end + relativedelta(
                    days=recurring_invoicing_offset + 1
                )
        else:  # pre-paid
            if recurring_invoicing_offset > 0:
                rnd = next_period_date_start + relativedelta(
                    days=recurring_invoicing_offset - 1
                )
            else:
                rnd = next_period_date_start + relativedelta(
                    days=recurring_invoicing_offset
                )
        if max_date_end and rnd > max_date_end:
            return False
        return rnd

    @api.depends(
        "last_date_invoiced",
        "date_start",
        "date_end",
        "recurring_invoicing_type",
        "recurring_invoicing_offset",
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
                # Recompute from date_start each step so the original
                # day-of-month is preserved through short months (e.g.
                # day 30 doesn't get clamped to 28 by February).
                n = 0
                while n < 10000:
                    period_start = rec.date_start + n * delta
                    if period_start > rec.last_date_invoiced:
                        break
                    n += 1
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
        if self.recurring_invoicing_type == "post-paid":
            delta = self.get_relative_delta(
                self.recurring_rule_type, self.recurring_interval
            )
            period_end = (
                self.next_period_date_start
                + delta
                - relativedelta(days=1)
            )
            days = (self.recurring_next_date - period_end).days
            if days > 1:
                new_offset = days
            elif days == 1:
                # rnd == period_end + 1, ambiguous between offset 0 and 1
                new_offset = (
                    1 if self.recurring_invoicing_offset >= 1 else 0
                )
            elif days == 0:
                # rnd == period_end, only offset -1 produces this
                new_offset = -1
            else:  # days < 0
                new_offset = days - 1
        else:  # pre-paid
            days = (
                self.recurring_next_date - self.next_period_date_start
            ).days
            if self.recurring_invoicing_offset > 0:
                new_offset = days + 1
            elif self.recurring_invoicing_offset < 0:
                new_offset = days
            else:  # current offset == 0, disambiguate by sign of days
                new_offset = days + 1 if days > 0 else days
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


class ContractLine(models.Model):
    _inherit = "contract.line"

    @api.constrains(
        "date_start", "date_end", "last_date_invoiced", "recurring_next_date"
    )
    def _check_last_date_invoiced(self):
        """For pre-paid with offset <= 0, the next invoice legitimately lands
        on or before last_date_invoiced (the period_end just invoiced), since
        the invoice for period N+1 happens at/before its start, which falls
        inside period N. Skip only that specific sub-check in those cases;
        all other sub-checks still apply."""
        relaxed = self.filtered(
            lambda r: (
                r.recurring_invoicing_type == "pre-paid"
                and r.recurring_invoicing_offset <= 0
            )
        )
        super(ContractLine, self - relaxed)._check_last_date_invoiced()
        for rec in relaxed.filtered("last_date_invoiced"):
            if rec.date_end and rec.date_end < rec.last_date_invoiced:
                raise ValidationError(
                    _(
                        "You can't have the end date before the date of "
                        "last invoice for the contract line '%s'"
                    )
                    % rec.name
                )
            if not rec.contract_id.line_recurrence:
                continue
            if rec.date_start and rec.date_start > rec.last_date_invoiced:
                raise ValidationError(
                    _(
                        "You can't have the start date after the date of "
                        "last invoice for the contract line '%s'"
                    )
                    % rec.name
                )