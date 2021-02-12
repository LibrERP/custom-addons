# -*- coding: utf-8 -*-
# © 2014-2021 Andrei Levin - Didotech srl (www.didotech.com)

{
    'name': 'Core Extended',
    'version': '12.0.5.3',
    'category': 'core',
    'author': 'Didotech Srl',
    'website': 'https://github.com/LibrERP/custom-addons',
    'depends': [
        'base',
        'mail'
    ],
    'data': [
        'views/ir_cron_view.xml'
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    "external_dependencies": {
        'python': [
            "openpyxl",
        ],
    }
}