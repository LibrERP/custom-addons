# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Account Fix',
    'version': '12.0.0.0',
    'category': 'Accounting',
    'summary': """Module solve the problem with the new invoice 
    being created with Sailsperson equal to active user instead of
    copying from original invoice""",
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account'
    ],
    'data': [
        # 'views/xxx_views.xml'
    ],
}
