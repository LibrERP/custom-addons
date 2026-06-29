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

    # Number of deltas next_period_date_start is shifted away from its
    # naive value. Written by the inverse on recurring_next_date (when
    # the user picks a date that requires a shift to preserve the
    # offset's sign). Orthogonal to recurring_invoicing_offset: editing
    # the offset keeps the period (and this shift) fixed and only moves
    # recurring_next_date; only editing recurring_next_date changes the
    # shift. Plain Integer (not a compute field) so onchange writes
    # propagate to the form without any compute-precedence surprises.
    next_period_date_start_shift = fields.Integer(
        default=0,
        copy=False,
    )
    next_period_date_start = fields.Date(
        compute="_compute_next_period_date_start",
        store=True,
    )
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

    def _naive_next_period_date_start(self):
        """The 'natural' next period_start: smallest period in the
        recurrence sequence after last_date_invoiced (or date_start
        itself when nothing's been invoiced yet)."""
        self.ensure_one()
        if not self.date_start:
            return False
        period_start = self.date_start
        if self.last_date_invoiced:
            delta = self.get_relative_delta(
                self.recurring_rule_type, self.recurring_interval
            )
            # Recompute from date_start each step so the original
            # day-of-month is preserved through short months (e.g.
            # day 30 doesn't get clamped to 28 by February).
            n = 0
            while n < 10000:
                period_start = self.date_start + n * delta
                if period_start > self.last_date_invoiced:
                    break
                n += 1
        if self.date_end and period_start > self.date_end:
            return False
        return period_start

    @api.depends(
        "last_date_invoiced",
        "date_start",
        "date_end",
        "recurring_rule_type",
        "recurring_interval",
        "next_period_date_start_shift",
    )
    def _compute_next_period_date_start(self):
        """Naive walk to the first period_start after last_date_invoiced,
        then apply next_period_date_start_shift (in deltas) to allow the
        inverse on recurring_next_date to express a user-requested shift
        without making the period writable directly."""
        for rec in self:
            naive = rec._naive_next_period_date_start()
            if not naive:
                rec.next_period_date_start = False
                continue
            if rec.next_period_date_start_shift:
                delta = rec.get_relative_delta(
                    rec.recurring_rule_type, rec.recurring_interval
                )
                rec.next_period_date_start = (
                    naive
                    + rec.next_period_date_start_shift * delta
                )
            else:
                rec.next_period_date_start = naive

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

    def _compute_shift_and_offset_for_rnd(self, rnd):
        """Pure (no-write) version of _derive: given a target rnd date,
        return (shift, new_offset) preserving the sign of the existing
        offset. Returns (None, None) if it can't derive (no date_start
        or no naive period)."""
        self.ensure_one()
        if not rnd:
            return (None, None)
        naive_period_start = self._naive_next_period_date_start()
        if not naive_period_start:
            return (None, None)
        period_start = naive_period_start
        shift = 0
        delta = self.get_relative_delta(
            self.recurring_rule_type, self.recurring_interval
        )
        current = self.recurring_invoicing_offset

        def shift_forward(ps, sh):
            return ps + delta, sh + 1

        def shift_backward(ps, sh):
            candidate = ps - delta
            if self.date_start and candidate < self.date_start:
                return None, sh
            return candidate, sh - 1

        if self.recurring_invoicing_type == "post-paid":
            def period_end_of(ps):
                return ps + delta - relativedelta(days=1)

            def next_period_end_of(ps):
                return ps + 2 * delta - relativedelta(days=1)

            if current >= 1:
                guard = 0
                while rnd <= period_end_of(period_start) and guard < 10000:
                    candidate, new_shift = shift_backward(
                        period_start, shift
                    )
                    if candidate is None:
                        break
                    period_start, shift = candidate, new_shift
                    guard += 1
                guard = 0
                while (
                    rnd > next_period_end_of(period_start)
                    and guard < 10000
                ):
                    period_start, shift = shift_forward(
                        period_start, shift
                    )
                    guard += 1
            elif current <= -1:
                guard = 0
                while rnd > period_end_of(period_start) and guard < 10000:
                    period_start, shift = shift_forward(
                        period_start, shift
                    )
                    guard += 1
                guard = 0
                while rnd < period_start and guard < 10000:
                    candidate, new_shift = shift_backward(
                        period_start, shift
                    )
                    if candidate is None:
                        break
                    period_start, shift = candidate, new_shift
                    guard += 1
            period_end = period_end_of(period_start)
            days = (rnd - period_end).days
            if days > 1:
                new_offset = days
            elif days == 1:
                new_offset = 1 if current >= 1 else 0
            elif days == 0:
                new_offset = -1
            else:
                new_offset = days - 1
        else:  # pre-paid
            if current >= 1:
                guard = 0
                while rnd < period_start and guard < 10000:
                    candidate, new_shift = shift_backward(
                        period_start, shift
                    )
                    if candidate is None:
                        break
                    period_start, shift = candidate, new_shift
                    guard += 1
                guard = 0
                while rnd >= period_start + delta and guard < 10000:
                    period_start, shift = shift_forward(
                        period_start, shift
                    )
                    guard += 1
            elif current <= -1:
                guard = 0
                while rnd >= period_start and guard < 10000:
                    period_start, shift = shift_forward(
                        period_start, shift
                    )
                    guard += 1
                guard = 0
                while rnd < period_start - delta and guard < 10000:
                    candidate, new_shift = shift_backward(
                        period_start, shift
                    )
                    if candidate is None:
                        break
                    period_start, shift = candidate, new_shift
                    guard += 1
            days = (rnd - period_start).days
            if current > 0:
                new_offset = days + 1
            elif current < 0:
                new_offset = days
            else:
                new_offset = days + 1 if days > 0 else days
        return (shift, new_offset)

    def _derive_offset_from_recurring_next_date(self):
        """Derive offset from current recurring_next_date, preserving
        the sign of the existing offset AND keeping |offset| within one
        delta. Walk period_start (starting from the naive value)
        forward/backward by deltas until rnd falls in the right period:
          - pre-paid positive: rnd inside current period (period_start
            <= rnd < period_start + delta);
          - pre-paid negative: rnd inside previous period (period_start
            - delta <= rnd < period_start);
          - post-paid positive: rnd inside next period (period_end <
            rnd <= period_end + delta);
          - post-paid negative: rnd inside current period (period_start
            <= rnd <= period_end).
        Writes the resulting offset AND the shift count (in deltas from
        the naive period_start). Backward walks are capped at date_start;
        if no shift can satisfy the sign, the natural (possibly flipped)
        value is used."""
        self.ensure_one()
        if not self.recurring_next_date:
            return
        naive_period_start = self._naive_next_period_date_start()
        if not naive_period_start:
            return
        rnd = self.recurring_next_date
        period_start = naive_period_start
        shift = 0
        delta = self.get_relative_delta(
            self.recurring_rule_type, self.recurring_interval
        )
        current = self.recurring_invoicing_offset

        def shift_forward(ps, sh):
            return ps + delta, sh + 1

        def shift_backward(ps, sh):
            candidate = ps - delta
            if self.date_start and candidate < self.date_start:
                return None, sh
            return candidate, sh - 1

        if self.recurring_invoicing_type == "post-paid":
            # Use period_start-based arithmetic for both bounds: adding
            # delta to period_end (e.g. Feb 28 + 1m = Mar 28) loses
            # month-end alignment, but period_start + N*delta does not.
            def period_end_of(ps):
                return ps + delta - relativedelta(days=1)

            def next_period_end_of(ps):
                return ps + 2 * delta - relativedelta(days=1)

            if current >= 1:
                # rnd in (period_end, next_period_end]
                guard = 0
                while rnd <= period_end_of(period_start) and guard < 10000:
                    candidate, new_shift = shift_backward(
                        period_start, shift
                    )
                    if candidate is None:
                        break
                    period_start, shift = candidate, new_shift
                    guard += 1
                guard = 0
                while (
                    rnd > next_period_end_of(period_start)
                    and guard < 10000
                ):
                    period_start, shift = shift_forward(period_start, shift)
                    guard += 1
            elif current <= -1:
                # rnd in [period_start, period_end]
                guard = 0
                while rnd > period_end_of(period_start) and guard < 10000:
                    period_start, shift = shift_forward(period_start, shift)
                    guard += 1
                guard = 0
                while rnd < period_start and guard < 10000:
                    candidate, new_shift = shift_backward(
                        period_start, shift
                    )
                    if candidate is None:
                        break
                    period_start, shift = candidate, new_shift
                    guard += 1
            period_end = period_end_of(period_start)
            days = (rnd - period_end).days
            if days > 1:
                new_offset = days
            elif days == 1:
                new_offset = 1 if current >= 1 else 0
            elif days == 0:
                new_offset = -1
            else:
                new_offset = days - 1
        else:  # pre-paid
            if current >= 1:
                # rnd in [period_start, period_start + delta)
                guard = 0
                while rnd < period_start and guard < 10000:
                    candidate, new_shift = shift_backward(
                        period_start, shift
                    )
                    if candidate is None:
                        break
                    period_start, shift = candidate, new_shift
                    guard += 1
                guard = 0
                while rnd >= period_start + delta and guard < 10000:
                    period_start, shift = shift_forward(period_start, shift)
                    guard += 1
            elif current <= -1:
                # rnd in [period_start - delta, period_start)
                guard = 0
                while rnd >= period_start and guard < 10000:
                    period_start, shift = shift_forward(period_start, shift)
                    guard += 1
                guard = 0
                while rnd < period_start - delta and guard < 10000:
                    candidate, new_shift = shift_backward(
                        period_start, shift
                    )
                    if candidate is None:
                        break
                    period_start, shift = candidate, new_shift
                    guard += 1
            days = (rnd - period_start).days
            if current > 0:
                new_offset = days + 1
            elif current < 0:
                new_offset = days
            else:
                new_offset = days + 1 if days > 0 else days
        # Write shift first so next_period_date_start re-derives via its
        # @api.depends before the offset write triggers rnd's recompute.
        # In write/inverse context use an explicit self.write() so the
        # value is actually persisted to DB (attribute assignment in an
        # inverse method can get clobbered by subsequent depends-driven
        # computes — notably upstream's _set_recurrence_field for
        # line_recurrence=False, which copies rnd from contract back to
        # line). In onchange/NewId context, fall back to attribute
        # assignment because write() doesn't apply to virtual records.
        in_onchange = not isinstance(self.id, int)
        vals = {"next_period_date_start_shift": shift}
        if current != new_offset:
            vals["recurring_invoicing_offset"] = new_offset
        if in_onchange:
            for fname, value in vals.items():
                setattr(self, fname, value)
        else:
            self.write(vals)

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

    def write(self, vals):
        """Two write-time fixups:
        1. When invoicing advances last_date_invoiced, drop any
           outstanding period shift so the natural cadence resumes
           (otherwise a shift of e.g. +1 would skip a period every
           billing cycle).
        2. When recurring_next_date is being written without an
           accompanying shift, derive the shift and offset inline and
           inject them into the same write call. Doing the derivation
           here (rather than relying on the inverse on rnd) makes the
           shift+offset+rnd values land atomically in super().write(),
           so they can't be clobbered by upstream depends-driven
           recomputes that run after the inverse — notably
           contract.line._set_recurrence_field copying rnd from
           contract.rnd when line_recurrence=False."""
        if (
            "last_date_invoiced" in vals
            and "next_period_date_start_shift" not in vals
        ):
            vals = dict(vals, next_period_date_start_shift=0)
        if (
            "recurring_next_date" in vals
            and "next_period_date_start_shift" not in vals
            and vals.get("recurring_next_date")
        ):
            rnd_val = vals["recurring_next_date"]
            if isinstance(rnd_val, str):
                rnd_val = fields.Date.from_string(rnd_val)
            # Records may have different naive periods, so apply
            # per-record. Each per-record write still goes through this
            # override but takes the early-out branch above (shift in
            # vals).
            if len(self) > 1:
                result = True
                for rec in self:
                    result = (
                        rec.write(dict(vals)) and result
                    )
                return result
            shift, new_offset = self._compute_shift_and_offset_for_rnd(
                rnd_val
            )
            if shift is not None:
                vals = dict(vals)
                vals["next_period_date_start_shift"] = shift
                if (
                    new_offset is not None
                    and "recurring_invoicing_offset" not in vals
                    and new_offset != self.recurring_invoicing_offset
                ):
                    vals["recurring_invoicing_offset"] = new_offset
        return super().write(vals)


class ContractLine(models.Model):
    _inherit = "contract.line"

    @api.depends(
        "contract_id.recurring_next_date",
        "contract_id.line_recurrence",
        "next_period_date_start_shift",
    )
    def _compute_recurring_next_date(self):
        """Upstream (abstract_contract_line) overrides rnd's compute to
        copy contract.rnd onto line.rnd when line_recurrence=False (via
        _set_recurrence_field). That clobbers any rnd value that
        belongs to a line with a manual period shift — e.g. the user
        edits line.rnd to Jun 4 (which sets shift=-1), saves, and
        upstream's compute immediately reverts line.rnd to contract.rnd
        (Jul 5). Run the upstream chain first, then for lines whose
        shift was set by the inverse, re-derive rnd from line.period
        +line.offset to make line.rnd reflect the manual shift instead
        of the contract header value."""
        super()._compute_recurring_next_date()
        shifted = self.filtered("next_period_date_start_shift")
        for rec in shifted:
            rec.recurring_next_date = self.get_next_invoice_date(
                rec.next_period_date_start,
                rec.recurring_invoicing_type,
                rec.recurring_invoicing_offset,
                rec.recurring_rule_type,
                rec.recurring_interval,
                max_date_end=rec.date_end,
            )

    def _get_period_to_invoice(
        self, last_date_invoiced, recurring_next_date, stop_at_date_end=True
    ):
        """Use next_period_date_start/end as the invoiced period so the
        markers (#START#/#END#) on generated invoice/sale lines honor any
        active period shift.

        Upstream derives first_date_invoiced from last_date_invoiced + 1
        day, which assumes a contiguous cadence. When the user has shifted
        the next period away from the natural cadence (e.g. the previous
        cycle ended 01/06 but the next period was shifted to start 01/07),
        upstream renders the stale start 02/06 while period_end and rnd
        already reflect the shifted period — producing e.g.
        "Dal 02/06 al 31/07" instead of "Dal 01/07 al 31/07".

        next_period_date_start already incorporates the shift, and
        next_period_date_end is the matching period end (period_start +
        delta - 1, clamped to date_end) — the same value
        _update_recurring_next_date writes to last_date_invoiced after
        invoicing, so the period we render stays consistent with how the
        cursor advances. We deliberately read next_period_date_end rather
        than re-deriving the end from rnd via the reverse formula, which
        uses upstream's offset convention and would be off by one day for
        positive offsets.
        """
        self.ensure_one()
        if not recurring_next_date:
            return False, False, False
        first_date_invoiced = self.next_period_date_start
        if not first_date_invoiced:
            return super()._get_period_to_invoice(
                last_date_invoiced, recurring_next_date, stop_at_date_end
            )
        if stop_at_date_end:
            # next_period_date_end is already clamped to date_end.
            last_date_invoiced = self.next_period_date_end
        else:
            last_date_invoiced = self.get_next_period_date_end(
                first_date_invoiced,
                self.recurring_rule_type,
                self.recurring_interval,
                max_date_end=False,
            )
        return first_date_invoiced, last_date_invoiced, recurring_next_date

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
