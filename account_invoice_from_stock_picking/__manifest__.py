# © 2022-2023 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Account Invoice From Stock Picking',
    'version': '12.0.2.10',
    'category': 'Accounting',
    'summary': 'Create Invoice from received Stock Pickings',
    'author': 'LibrERP',
    'website': 'https://www.librerp.it',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'account',
        'stock',
        'base_view_inheritance_extension',
        'stock_picking_invoice_link'  # OCA: stock-logistics-workflow
    ],
    'data': [
        'views/stock_picking.xml',
        'views/stock_move.xml',
        # 'views/purchase_order_line.xml',
        'wizard/invoice_from_picking_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
