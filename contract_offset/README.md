# Contract offset

Lets `recurring_invoicing_offset` be edited freely on a contract line, with
the meaning of the value determined by its sign. Periods march
calendar-aligned from `date_start`.

## Offset semantics

| Sign | Meaning |
|---|---|
| **positive (>=1)** | Day N inside the relevant period |
| **zero** | First day of the relevant period (same as offset 1) |
| **negative (<=-1)** | N days before the start of the period that follows the anchor period |

The "relevant period" depends on `recurring_invoicing_type`:

- **pre-paid** — invoice falls in the current service period
- **post-paid** — invoice falls in the next period (one delta forward)

## Period sequence

Periods march from `date_start` by one recurrence delta each.

Example with `date_start = 01.01.2026`, monthly:

```
01.01 - 31.01,  01.02 - 28.02,  01.03 - 31.03,
01.04 - 30.04,  01.05 - 31.05,  01.06 - 30.06, ...
```

`next_period_date_start` = the first period in that sequence that comes
after `last_date_invoiced`. The exact day of `last_date_invoiced` doesn't
matter — periods stay calendar-aligned.

## Formula
period_start - start of the period to be invoiced
next_period_start - period after current period

```
pre-paid                            post-paid (one period forward)
-----------------------------       --------------------------------------
offset > 0: period_start + (N-1)    offset > 0: next_period_start + (N-1)
offset = 0: period_start            offset = 0: next_period_start
offset < 0: next_period_start + N   offset < 0: period_after_next_start + N
```

## Examples

Monthly, `date_start = 01.01.2026`, looking at the May service period
(`01.05 - 31.05`):

| offset | pre-paid `recurring_next_date` | post-paid `recurring_next_date` |
|---:|:---:|:---:|
| 1   | 01.05 | 01.06 |
| 28  | 28.05 | 28.06 |
| 30  | 30.05 | 30.06 |
| -1  | 31.05 | 30.06 |
| -3  | 29.05 | 28.06 |
| -4  | 28.05 | 27.06 |
| -30 | 02.05 | 01.06 |

## Editing behaviour

- Edit `recurring_invoicing_offset` → `recurring_next_date` recomputes via
  the formula above (compute fires on the form via `@api.depends`).
- Edit `recurring_next_date` → offset is derived. The **sign of the current
  offset is preserved**, so the user controls the +/- convention — e.g.
  with offset = -4 currently, typing `27.05` flips offset to -5 (still
  negative); with offset = 28, typing `27.05` flips offset to 27 (still
  positive). Both an `inverse` (write) and an `@api.onchange` (live form)
  handle this.
- `last_date_invoiced` stays readonly; only the invoicing flow writes it.
- After invoicing, the period sequence advances and `recurring_next_date`
  recomputes automatically with the same offset.

## Files

- `models/contract_recurrency_mixin.py` — overrides
  `contract.recurrency.basic.mixin` (makes offset stored + editable) and
  `contract.recurrency.mixin` (period sequence, formula, inverse, onchange).