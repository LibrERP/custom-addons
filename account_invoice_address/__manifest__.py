# © 2023 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Account Invoice Address',
    'version': '12.0.0.0',
    'category': 'Accounting',
    'summary': """
        Main Address: Hide non main addresses
        Shipping Address: show only addresses related to main address
    
    """,
    'author': 'LibrERP',
    'website': 'https://www.librerp.it',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'account',
        'sale'
    ],
    'data': [
        'views/account_invoice_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
