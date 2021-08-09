# -*- coding: utf-8 -*-
# © 2015-2017 Didotech srl (www.didotech.com)
{
    'name': 'Data migration import',
    'version': '12.0.0.0',
    'category': 'Tools',
    'author': 'powERP enterprise network',
    'website': 'https://www.powerp.it',
    'development_status': 'Alpha',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'core_extended',
        'product',
    ],
    'external_dependencies': {'python': ['xlrd']},
    'data': [
        'wizard/file_import_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
