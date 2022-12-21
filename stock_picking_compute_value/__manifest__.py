# © 2021-2022 Marco Tosato (Didotech srl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Compute stock picking value',
    'summary': 'Compute value of the stock picking as sum of the value of the single lines',
    'description': '''
        Compute the total amount, base amount and total tax amount for the stock picking.
        The computation is based on source values in the related sale.order
    ''',
    'version': '12.0.1.0.1',
    'author': 'Didotech srl',
    'website': 'https://www.didotech.com',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'stock',
        'sale',
    ],
    'data': [
    ],
    'application': False,
    'installable': True,
}
