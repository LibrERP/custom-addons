# © 2023 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Purchase Order Readonly',
    'version': '16.0.0.0.0',
    'category': 'Inventory/Purchase',
    'summary': 'Set Qty and Price in Readonly when RFQ is confirmed',
    "author": "Didotech srl",
    'website': 'https://www.didotech.com',
    'depends': [
        'base',
        'purchase'
    ],
    'data': [
        "views/purchase_view.xml",
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3'
}
