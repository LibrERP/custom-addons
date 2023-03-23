# © 2022-2023 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Account Invoice From Stock Picking II',
    'version': '12.0.2.23',
    'category': 'Accounting',
    'summary': """Create Invoice from received Stock Pickings.
    Set existing invoice where new lines should be added or create a new one.
    Set or correct product price and discount.
    """,
    'author': 'LibrERP',
    'website': 'https://www.librerp.it',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'account',
        'stock',
        'base_view_inheritance_extension',
        'stock_picking_invoice_link',  # OCA: stock-logistics-workflow
        'l10n_it_ddt'  # OCA: l10n-italy
    ],
    'data': [
        'views/stock_picking.xml',
        'views/stock_move.xml',
        'wizard/invoice_from_picking_view.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
