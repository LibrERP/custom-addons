# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Sale Project Fix',
    'version': '18.0.0.0',
    'category': 'Sale',
    'summary': 'Module solves the problem with setting the project on an Order without setting the project on Order Lines',
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
