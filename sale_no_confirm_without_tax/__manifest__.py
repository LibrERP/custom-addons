# © 2025 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Sale Order block confirm without tax',
    'version': '16.0.0.1',
    'category': 'Sales',
    'summary': 'Block confirmation of an Order if it contains lines without any tax',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'sale'
    ],
    'data': [
        'views/sale_views.xml'
    ],
}
