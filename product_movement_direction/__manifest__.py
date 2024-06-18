# © 2024 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Product Movement Direction',
    'version': '16.0.0.1',
    'category': 'Stock',
    'summary': 'Add column with +/- to show if product arrives or departuring',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'stock'
    ],
    'data': [
        'views/stock_views.xml'
    ],
}
