# -*- coding: utf-8 -*-
{
    'name': "Italian localization - fiscal Document Type Improved",

    'summary': """
        Improvements for module l10n_it_fiscal_document_type""",

    'description': """
        Improvements for module l10n_it_fiscal_document_type:
        automatic document recognition based on DDT date
    """,

    'author': "Powerp",
    'website': "https://www.powerp.it",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Localisation/Italy',
    'version': '0.1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'l10n_it_fiscal_document_type'
    ],

    # always loaded
    'data': [
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
