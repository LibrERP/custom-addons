# © 2025 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'ITA - Ricezione e-fattura Search fix',
    'version': '16.0.0.0',
    'category': 'Hidden',
    'summary': 'Remove restriction that excludes self invoices from list',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'l10n_it_fatturapa_in'
    ],
    'data': [
        'views/account_views.xml'
    ],
}
