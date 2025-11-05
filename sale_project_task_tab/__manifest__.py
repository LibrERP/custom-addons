# © 2025 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Task tab in Sale Order',
    'version': '18.0.0.0',
    'category': 'Project',
    'summary': 'Module adds Task tab inside Sale Order',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'sale',
        'sale_project',
        'project'
    ],
    'data': [
        'views/sale_order_views.xml'
    ],
}
