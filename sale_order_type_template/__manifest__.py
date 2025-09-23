# © 2025 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Sale Order Type Template',
    'version': '16.0.0.1',
    'category': 'Sales',
    'summary': 'Module creates a connection between Order Type and Order Template',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'sale_order_type',  # OCA/sale-workflow
        'sale_management',  # Odoo
    ],
    'data': [
        'views/sale_order_type_views.xml'
    ],
}
