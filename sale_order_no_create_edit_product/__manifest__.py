# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Sale Order no Create Edit Product',
    'version': '16.0.0.0',
    'category': 'Sales',
    'summary': 'Module disable the possibility to create or modify product from Sale Order Line',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'sale'
    ],
    'data': [
        'views/sale_order_views.xml'
    ],
}
