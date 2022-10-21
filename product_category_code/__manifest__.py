# © 2022 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    "name": "Add Code in Product Category",
    "version": "12.0.0.2",
    "category": "Sales Management",
    "description": """
        This module adds Code on Product Category.
    """,
    "author": "Didotech Srl",
    "depends": [
        'product'
    ],
    "data": [
        "views/product_category_view.xml",
        "views/product.xml"
    ],
    "auto_install": False,
    "installable": True,
}
