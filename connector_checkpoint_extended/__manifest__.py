# © 2020 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "connector_checkpoint_extended",

    'summary': """
        Module extends functionality of connector's checkpoints""",

    'description': """
        Module extends functionality of connector's checkpoints
    """,

    'author': "Didotech srl",
    'website': "http://www.didotech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Connector',
    'version': '0.0.1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'connector'
    ],

    # always loaded
    'data': [
        'views/checkpoint_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
