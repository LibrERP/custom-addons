# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Account Journal Payment Bank',
    'version': '16.0.0.2',
    'category': 'Accounting',
    'summary': 'Module adds payment bank to Account Journal which is used when creating an Invoice',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account',
        'l10n_it_riba',
    ],
    'data': [
        'views/account_journal_views.xml'
    ],
}
