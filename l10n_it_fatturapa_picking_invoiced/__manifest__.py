# © 2023 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Stock Picking Invoiced',
    'version': '12.0.0.0',
    'category': 'Accounting',
    'summary': 'Set Picking to Invoice when Invoice is created from XML already connected to Stock Picking',
    'author': 'LibrERP',
    'website': 'https://www.librerp.it',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'account_invoice_from_stock_picking',
        'l10n_it_fatturapa_in'
    ],
    'data': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
