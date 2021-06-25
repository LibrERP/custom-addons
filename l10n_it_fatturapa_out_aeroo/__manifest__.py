# -*- coding: utf-8 -*-
{
    'name': "l10n_it_fatturapa_out_extended",

    'summary': """
        Module extends functionality of fatturapa_out wizard """,

    'description': """
        Module extends functionality of fatturapa_out wizard
    """,

    'author': "Didotech Srl",
    'website': "http://www.didotech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customization',
    'version': '12.0.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'l10n_it_fatturapa_out',
                'report_aeroo',
                'report_aeroo_invoice']
}
