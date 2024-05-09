# © 2024 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Partner Notes in DDT',
    'version': '12.0.0.1',
    'category': 'Stock',
    'summary': 'Notes added in the Contact will be shown in Stock Picking and DDT',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'stock',
        'l10n_it_ddt',
        'stock_picking_package_preparation'
    ],
    'data': [
        'views/partner_views.xml',
        'views/stock_views.xml'
    ],
}
