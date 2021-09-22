# -*- coding: utf-8 -*-
{
    'name': "Dashboard Utenti",

    'summary': """
        Modulo per la verifica dei lavori in corso di sviluppo dagli utenti""",

    'description': """
        Modulo per la verifica dei lavori in corso di sviluppo dagli utenti
    """,

    'author': "Didotech S.r.l.",
    'website': "https://www.didotech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Project Management',
    'version': '12.0.1.1.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/res_config.xml'
    ],
}