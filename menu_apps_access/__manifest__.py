# © 2024 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Limit access to Apps menu',
    'version': '16.0.0.0',
    'category': 'Hidden',
    'summary': 'Limit access to Apps menu to System Administrator',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'base_install_request'
    ],
    'data': [
        'views/menu_views.xml'
    ],
}
