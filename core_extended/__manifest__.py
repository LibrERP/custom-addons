# © 2014-2021 Didotech srl (<http://www.didotech.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Core Extended',
    'version': '14.0.5.3',
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
    'installable': False,
    'application': True,
    'auto_install': False,
    "external_dependencies": {
        'python': [
            "openpyxl",
        ],
    }
}
