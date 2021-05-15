# -*- coding: utf-8 -*-
{
    'name': "Italian localization - l10n_it_fatturapa_in_improved",

    'summary': """
        Corrections to official l10n_it_fatturapa_in""",

    'description': """
        Module make some improvements to official l10n_it_fatturapa_in:
        - Added columnn with SDI date
    """,

    'author': "Powerp",
    'website': "https://www.powerp.it",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Localisation/Italy',
    'version': '0.3.1',
    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'l10n_it_fatturapa_in'
    ],

    # always loaded
    'data': [
        'views/attachment_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml'
    ]
}
