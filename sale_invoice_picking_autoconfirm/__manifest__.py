# © 2025 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Sale Order to Invoice, Picking Autoconfirm',
    'version': '16.0.0.2',
    'category': 'Sale',
    'summary': 'Autoconfirm Picking when creating Invoice from Sale Order',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'sale',
        'sale_stock',
        'account'
    ],
    'data': [
        'wizard/sale_make_invoice_advance_view.xml'
    ],
}
