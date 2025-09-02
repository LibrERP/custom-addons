# © 2025 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Sale Order Type Tax ',
    'version': '16.0.0.0',
    'category': 'Sales Management',
    'summary': 'Module permits to set default tax for selected document type',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'sale_order_type'  # OCA/sale-workflow
    ],
    'data': [
        'views/sale_order_type_views.xml'
    ],
}
