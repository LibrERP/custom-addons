# © 2023 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    'name': 'Purchase Requisition Enhanced',
    'version': '0.1.0.2',
    'category': 'Inventory/Purchase',
    'description': """
This module solve some problems in Purchase Requisition module
==============================================================

Solve problem with multiple presence of the same product in the same order which is not handled correctly
""",
    'depends': [
        'purchase_requisition'
    ],
    'data': [
        'views/purchase_view.xml',
    ],
    'license': 'LGPL-3',
}
