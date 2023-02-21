# © 2023 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    "name": "Show Invoice Status in Purchase Order List",
    "version": "12.0.0.0",
    "category": "Purchase Management",
    "description": """
        This module shows Invoice Status column in Purchase Order List.
    """,
    "author": "Didotech Srl",
    "depends": [
        'purchase'
    ],
    "data": [
        "views/purchase_order_view.xml",
    ],
    "auto_install": False,
    "installable": True,
}
