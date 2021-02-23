# -*- coding: utf-8 -*-
{
    'name': "Italian localization - Custom XML Tags",

    'summary': """
        Custom tags in Electronic Invoice XML""",

    'description': """
        Module permits to insert custom information as required by some industries, for example Amazon
    """,

    'author': "Powerp",
    'website': "https://www.powerp.it",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Localisation/Italy',
    'version': '0.3.4',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'l10n_it_fatturapa',
        'l10n_it_fatturapa_out',
        'product_customerinfo'
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/partner_view.xml',
        'views/sale_order_view.xml',
        # 'views/account_invoice_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
