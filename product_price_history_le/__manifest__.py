# © 2021-2022 Didotech srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    "name": "Product Price History",
    "version": "12.0.2.3",
    'author': 'Didotech srl, Moltis Technologies',
    'website': 'http://www.didotech.com',
    "license": "AGPL-3",
    "category": "Generic Modules/Inventory Control",
    "description": """Historial Price Products. List of historial Sale Price and Cost Price""",
    "depends": [
        "account",
        "product"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_price_history_view.xml",
        "views/product_view.xml",
    ],
    "active": False,
    "installable": True
}
