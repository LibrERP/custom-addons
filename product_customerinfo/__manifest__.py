# © 2020 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "product_customerinfo",

    'summary': """
        Module adds possibility to handle product codes for compliance with customer system""",

    'description': """
        Module adds possibility to handle product codes for compliance with customer system
    """,

    'author': "Powerp",
    'website': "https://www.powerp.it",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales Management',
    'version': '0.2.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'product'
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/product_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
