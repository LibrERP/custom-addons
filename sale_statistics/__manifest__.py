# © 2020-2023 Fabio Colognesi - Didotech srl
# © 2024-2026 Fabio Colognesi - Codebeex srl (www.codebeex.com)
#
#    Created on : 2020-11-26
#    Author : Fabio Colognesi
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Sale Statistics',
    'version': '18.0.1.0.0',
    'category': 'Sales/Sales',
    'author': 'Didotech srl',
    'website': 'https://www.codebeex.com',
    'development_status': 'Alpha - not tested in production',
    'license': 'LGPL-3',
    'depends': [
        'sale',
        'sale_stock',
        'sale_margin',
        'partner_region',
    ],
    'data': [
        'security/sale_statistics.xml',
        'security/account_security.xml',
        'security/ir.model.access.csv',
        'report/sale_report_view.xml',
        'data/scheduled_action.xml',
        'views/board_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
