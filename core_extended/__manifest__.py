# © 2014-2021 Didotech srl (<http://www.didotech.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Core Extended',
    'version': '12.0.5.3',
    'category': 'core',
    'author': 'powERP enterprise network',
    'website': 'https://www.powerp.it',
    'development_status': 'Alpha',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
    ],
    'external_dependencies': {'python': ['openpyxl']},
    'data': ['views/ir_cron_view.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
