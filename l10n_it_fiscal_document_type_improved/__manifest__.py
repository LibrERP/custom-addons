# -*- coding: utf-8 -*-
{
    'name': "Italian localization - fiscal Document Type Improved",

    'summary': """
        Improvements for module l10n_it_fiscal_document_type""",

    'description': """
        Improvements for module l10n_it_fiscal_document_type:
        automatic document recognition based on DDT date:
        if invoice is created in the same month as the Transportation Document,
            than document type is TD24 and the date of invoice is Today
        if TD is from previous month but we are in the first 10 days of the next month,
            than document type is TD24 but invoice date is the last day from the previous month
        All other cases it is TD25 and the date is Today 
    """,

    'author': "Powerp",
    'website': "https://www.powerp.it",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Localisation/Italy',
    'version': '0.6.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'l10n_it_fiscal_document_type',
        'l10n_it_ddt'
    ],

    # always loaded
    'data': [
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
