# © 2024 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Sale Order Product with Fee and Setup',
    'version': '12.0.0.0',
    'category': 'Sales',
    'summary': 'Add Fee and Setup products to main product. The Variant depends on quantity',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'product',
        'sale'
    ],
    'data': [
        'views/product_views.xml',
        'views/sale_views.xml'
    ],
}
