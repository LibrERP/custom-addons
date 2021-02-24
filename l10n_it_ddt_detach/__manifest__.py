# -*- coding: utf-8 -*-
# © 2021 Andrei Levin - Didotech srl (www.didotech.com)

{
    'name': 'l10n_it_ddt_detach',
    'summary': """
    Detach Invoice from TD""",
    'description': """
    Detach Invoice from TD to be able to create new Invoice. 
    Operation is required when wrong invoice was created and already send to SDI and new Invoice should be created
""",
    'version': '12.0.0.0',
    'category': 'Accounting',
    'author': 'Didotech Srl',
    'website': 'https://github.com/LibrERP/custom-addons',
    'depends': [
        'base',
        'account',
        'l10n_it_ddt'
    ],
    'data': [
        'views/stock_picking_package_preparation_view.xml',
        'wizard/wizard_detach_invoice_view.xml'
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    "external_dependencies": {}
}
