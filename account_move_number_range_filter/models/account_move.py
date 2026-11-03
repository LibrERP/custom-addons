# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    # Search-only helper: lets the invoice search view offer "Number ≥ / ≤"
    # range boxes that compare the document number (``name``) *within a single
    # series*. The field is not stored; its whole purpose is the custom
    # ``search`` method below.
    number_search = fields.Char(
        string="Number",
        compute="_compute_number_search",
        search="_search_number_range",
        help="Filter by document number with range operators, e.g. "
             "Number ≥ 2026/0432. The comparison is automatically scoped to "
             "the series prefix you type, so the 2026/… series is never mixed "
             "with PA/…, ACQ/…, NC/… etc.",
    )

    @api.depends("name")
    def _compute_number_search(self):
        for move in self:
            move.number_search = move.name

    def _search_number_range(self, operator, value):
        """Scope a numeric-style range comparison to one invoice series.

        ``account.move.name`` is a Char, so a bare ``name >= '2026/0432'`` is a
        *lexicographic* comparison: every letter-prefixed series ('PA/…',
        'ACQ/…', 'NC/…') sorts after the digit '2' and would leak into the
        result. Here we parse the typed value, derive its series prefix
        (everything up to and including the last '/'), and AND an ``=like``
        prefix constraint onto the comparison so only that series is matched::

            Number >= 2026/0432  ->  name =like '2026/%'  AND  name >= '2026/0432'
            Number <= PA/2026/30 ->  name =like 'PA/2026/%' AND name <= 'PA/2026/30'

        Within one zero-padded series this lexicographic range matches the
        numeric order the user expects.
        """
        ordering_operators = (">=", ">", "<=", "<")
        # Only the range operators get prefix-scoping; anything else (e.g. the
        # UI's default '=' / 'ilike') falls back to a plain name comparison.
        if operator not in ordering_operators or not isinstance(value, str):
            return [("name", operator, value)]

        prefix, separator, _counter = value.rpartition("/")
        if not separator:
            # No '/' in the typed value -> no series to scope to.
            return [("name", operator, value)]

        return [
            "&",
            ("name", "=like", prefix + "/%"),
            ("name", operator, value),
        ]
