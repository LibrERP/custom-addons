# © 2025 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'DDT in Sale Order',
    'version': '16.0.0.2',
    'category': 'Sales',
    'summary': 'DDT in Sale Order',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'sale_stock',
        'l10n_it_delivery_note'  # l10n-italy
    ],
    'data': [
        'views/sale_order_views.xml'
    ],
}
