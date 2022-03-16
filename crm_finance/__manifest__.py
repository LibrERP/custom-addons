# © 2022 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'CRM Finance',
    'version': '12.0.0.1',
    'category': 'Customer Relationship Management',
    'summary': 'Add more financial information in Opportunity (connected to existing Sale Order)',
    'author': 'LibrERP enterprise network',
    'website': 'https://www.librerp.it',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'crm',
        'sale_crm'
    ],
    'data': [
        'views/crm_lead_view.xml'
    ],
}
