# © 2022 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Account Invoice From Stock Picking',
    'version': '12.0.2.2',
    'category': 'Accounting',
    'summary': 'Create Invoice from received Stock Pickings',
    'author': 'LibrERP',
    'website': 'https://www.librerp.it',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'account',
        'stock'
    ],
    'data': [
        'wizard/invoice_from_picking_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
