# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Sale CRM/Lead Fields',
    'version': '18.0.0.0',
    'category': 'Sale',
    'summary': 'Module permits to see CRM/Lead fields in Sale Order',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'sale',
        'crm_enterprise'
    ],
    'data': [
        'views/sale_order_views.xml'
    ],
}
