# © 2021 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Account Invoice Inversion',
    'version': '12.0.2.0',
    'category': 'Accounting',
    'summary': 'Inverse sign in Account Invoice and transform it in Credit Note',
    'author': 'SHS-AV s.r.l.',
    'website': 'https://www.zeroincombenze.it',
    'development_status': 'Alpha',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'account',
    ],
    'external_dependencies': {},
    'data': ['views/account_invoice_view.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
