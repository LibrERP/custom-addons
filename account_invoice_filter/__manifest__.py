# © 2022-2023 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Account Invoice Additional Filters',
    'version': '12.0.0.0',
    'category': 'Accounting',
    'summary': """This module adds filters:,
    Last Month, Current Month and Next Month""",
    'author': 'Didotech srl',
    'website': 'https://www.didotech.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'account'
    ],
    'data': [
        'views/account_invoice_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
