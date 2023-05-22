# -*- coding: utf-8 -*-
{
    'name': "Massive DDT creation",

    'summary': """
        Create DDT from stock picking or sale orders selection""",

    'description': """
        Create DDT from stock picking or sale orders selection.
        Helps to save stock picking elaboration about quantities.
        Reduce errors creating DDT working directly from sale orders.
    """,

    'author': "Didotech Srl",
    'website': "http://www.didotech.com",
    'category': 'Stock',
    'version': '12.0.7.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'stock', 
        'l10n_it_ddt',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_view.xml',
        'wizard/massive_ddt_creation_wizard.xml',
    ]
}
