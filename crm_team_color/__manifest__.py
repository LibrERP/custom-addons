# © 2024 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'CRM Team Color',
    'version': '16.0.0.0',
    'category': 'Customer Relationship Management',
    'summary': 'Color CRM cards in Kanban',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'sales_team',
        'crm'
    ],
    'data': [
        'views/assets.xml',
        'views/crm_lead_views.xml',
        'views/crm_team_views.xml'
    ],
}
