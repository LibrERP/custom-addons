# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Italy - Supplier DDT Number on Receipts',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Localizations/EDI',
    'summary': "Record the supplier's DDT number on incoming pickings",
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'l10n_it_stock_ddt',
    ],
    'data': [
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}