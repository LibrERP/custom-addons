# © 2023 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Account Invoice Partner Filter',
    'version': '12.0.0.1',
    'category': 'Accounting',
    'summary': 'Filter Account Invoice by partner type',
    'author': 'Didotech s.r.l.',
    'website': 'https://www.didotech.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'account',
    ],
    'data': [
        'views/account_invoice_view.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
