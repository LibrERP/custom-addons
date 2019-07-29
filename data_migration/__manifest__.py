# -*- coding: utf-8 -*-
# © 2015-2017 Didotech srl (www.didotech.com)

{
    'name': 'Data migration import',
    'version': '12.0.0.0',
    'category': 'Tools',
    "author": "Didotech SRL",
    'website': 'http://www.didotech.com',
    'depends': [
        'base',
        'core_extended',
        'product',
    ],
    'data': [
        "wizard/file_import_view.xml",
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'external_dependencies': {
        'python': [
            'xlrd',
        ]
    }
}
