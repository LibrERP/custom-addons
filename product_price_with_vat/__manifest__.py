# © 2023 Didotech srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    "name": "Product Price With VAT",
    "version": "12.0.0.0",
    'author': 'Didotech srl, Moltis Technologies',
    'website': 'http://www.didotech.com',
    "license": "AGPL-3",
    "category": "Generic Modules/Inventory Control",
    "description": """Inside Product view show also price with VAT.""",
    "depends": [
        "account",
        "product"
    ],
    "data": [
        "views/product_view.xml",
    ],
    "active": False,
    "installable": True
}
