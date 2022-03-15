# © 2022 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Account Invoice 80 Lines',
    'version': '12.0.0.0',
    'category': 'Accounting',
    'summary': 'Show 80 lines in Account Invoice',
    'author': 'LibrERP',
    'website': 'https://www.librerp.it',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'account',
    ],
    'data': [
        'views/account_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
