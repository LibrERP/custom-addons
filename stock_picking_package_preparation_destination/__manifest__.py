# © 2023 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Stock Picking Package Preparation Destination',
    'version': '12.0.0.0',
    'category': 'Stock',
    'summary': 'Add destination address to Picking Package Preparation tree view',
    'author': 'LibrERP enterprise network',
    'website': 'https://www.librerp.it',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'stock',
        'partner_address',
        'l10n_it_ddt'  # OCA: l10n-italy

    ],
    'data': [
        'views/stock_picking_view.xml'
    ],
}
