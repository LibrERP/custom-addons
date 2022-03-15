# © 2022 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'l10n_it_ddt_sort_by_order',
    'version': '12.0.0.1',
    'category': 'Accounting',
    'summary': 'Sort stock.picking.package.preparation.line by Sale Order name and Sale Order Line order',
    'author': 'LibrERP',
    'website': 'https://www.librerp.it',
    'development_status': 'Alpha',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account',
        'l10n_it_ddt',
    ],
    'external_dependencies': {},
    'data': [
        # 'wizard/wizard_detach_invoice_view.xml',
        # 'views/stock_picking_package_preparation_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
