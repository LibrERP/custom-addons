# © 2023 Andrei Levin - Didotech srl (www.didotech.com)
# © 2024 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Account Invoice Address',
    'version': '16.0.0.0',
    'category': 'Accounting',
    'summary': """
        Main Address: Hide non main addresses
        Shipping Address: show only addresses related to main address
    
    """,
    'author': 'Codebeex',
    'website': 'https://github.com/LibrERP/custom-addons',
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
