# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Invoice Number Range Filter',
    'version': '18.0.0.1',
    'category': 'Accounting',
    'summary': "Filter invoices/journal entries by number with range operators "
               "(Number ≥ / Number ≤), e.g. Number ≥ 2026/0427",
    'description': """
Invoice Number Range Filter
===========================

Adds two search boxes to the invoice/bill search view:

* **Number ≥** — keep documents whose number is greater than or equal to
  the typed value (``[('name', '>=', self)]``).
* **Number ≤** — keep documents whose number is less than or equal to the
  typed value (``[('name', '<=', self)]``).

The invoice number (``account.move.name``) is a text field, so the comparison
is lexicographic. For zero-padded, consistently-formatted series this matches
numeric order (``2026/0001`` < ``2026/0427`` < ``2026/0999``).

IMPORTANT — scope the comparison to a single series. Because the numbers carry
different prefixes (``2026/…``, ``ACQ/…``, ``PA/…``, ``NC/…``) and letters sort
after digits in text, a ``Number ≥ 2026/0427`` filter used *alone* also matches
the letter-prefixed series. Pair it with a Journal filter (or type the full
prefix) to compare within one series.
""",
    'author': 'Codebeex srl',
    'website': 'https://github.com/LibrERP/custom-addons',
    'license': 'AGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'views/account_move_views.xml',
    ],
    'installable': True,
}
