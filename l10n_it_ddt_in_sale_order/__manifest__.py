# © 2025 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'DDT in Sale Order',
    'version': '16.0.0.0',
    'category': 'Sales',
    'summary': 'DDT in Sale Order',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        # 'sale',
        'sale_stock',
        'pos_sale',
        'point_of_sale'
    ],
    'data': [
        'views/sale_order_views.xml'
    ],
}
