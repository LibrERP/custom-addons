# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'HR User List',
    'version': '18.0.0.0',
    'category': 'Human Resources',
    'summary': 'Menu in Employees / Configuration listing users and their last access time',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'hr',
    ],
    'data': [
        'views/res_users_views.xml',
    ],
}
