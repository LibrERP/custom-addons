# © 2025 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Sale Order Restricted Confirm',
    'version': '12.0.0.0',
    'category': 'Sales',
    'summary': 'Module restricts access to Confirm button in Sale Order only to the members of dedicated group',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'sale'
    ],
    'data': [
        'data/groups.xml',
        'views/sale_views.xml'
    ],
}
