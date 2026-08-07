# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Account Move Analytic Filter',
    'version': '18.0.0.2',
    'category': 'Accounting',
    'summary': "Adds possibility to filter by Analytic account",
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account'
    ],
    'data': [
        'views/account_move_views.xml'
    ],
}
