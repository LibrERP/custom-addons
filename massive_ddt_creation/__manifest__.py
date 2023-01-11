# -*- coding: utf-8 -*-
{
    'name': "Massive DDT creation",

    'summary': """
        Create DDT from picking or orders selection""",

    'description': """
        Create DDT from picking or orders selection
    """,

    'author': "Didotech Srl",
    'website': "http://www.didotech.com",
    'category': 'Accounting',
    'version': '12.0.0.1.3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'l10n_it_ddt'],

    # always loaded
    'data': [
        'views/res_config_view.xml',
        'wizard/massive_ddt_creation_wizard.xml',
    ]
}
