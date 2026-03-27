# © 2025-2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'ITA - Emissione e-fattura FIX',
    'version': '16.0.0.1',
    'category': 'Hidden',
    'summary': 'Fix errors in out invoice composition',
    'description': """Module solve problems with the VAT composition for countries different from Italy.
        Also l'XML in the state 'sender_error' can be deleted without setting it to 'ready'
    """,
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'l10n_it_fatturapa_out'
    ],
    'data': [],
}
