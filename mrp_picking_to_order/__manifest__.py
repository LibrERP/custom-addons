# © 2022 Didotech srl (<http://www.didotech.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'MRP Stock Picking to Purchase Order',
    'version': '12.0.0.0.2',
    'category': 'MRP',
    "author": "Didotech SRL",
    'website': 'https://www.didotech.com',
    'depends': [
        'base',
        'stock'
    ],
    'data': [
        'views/stock_picking_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False
}
