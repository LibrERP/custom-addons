# Didotech s.r.l. 2023
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Invoice deposit',
    'version': '12.0.1.0.9',
    'category': 'Customization',
    'summary': 'Deposit into invoice',
    'author': 'Didotech s.r.l.',
    'website': 'https://www.didotech.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account',
        'l10n_it_account',
        'account_duedates',
    ],
    'data': [
        'views/account_invoice_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

