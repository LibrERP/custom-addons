# Copyright 2023 Didotech Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Web Export Current View',
    'version': '12.0.1.0.1',
    'category': 'Web',
    'author': 'Didotech Srl',
    'website': 'https://didotech.com',
    'license': 'AGPL-3',
    'depends': [
        'web',
        'web_export_view'
    ],
    "data": [
        'views/web_export_view_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
