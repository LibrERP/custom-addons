# © 2023 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Purchase Order Cancel Restricted',
    'version': '16.0.0.0.0',
    'category': 'Customer Relationship Management',
    'summary': 'Restricted access to Cancel button',
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
