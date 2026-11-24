# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Sale Project Fix',
    'version': '18.0.0.2',
    'category': 'Sale',
    'summary': 'Fixes for sale_project: set the Order project on its service lines; Sales Order Item dialog keeps the typed description and reuses an empty quotation',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'sale_project'
    ],
    'data': [
        'views/sale_order_views.xml'
    ],
}
