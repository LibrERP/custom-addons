# © 2023 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Purchase Remove Alternatives',
    'version': '16.0.0.0.0',
    'category': 'Inventory/Purchase',
    'summary': """Substitute button Cancel alternatives with the button Remove alternatives
               which deletes discarded lines""",
    "author": "Didotech srl",
    'website': 'https://www.didotech.com',
    'depends': [
        'base',
        'purchase',
        'purchase_requisition'
    ],
    'data': [
        "wizard/purchase_requisition.xml",
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3'
}
