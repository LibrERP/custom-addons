# © 2022 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Sale Order connect Invoice',
    'version': '12.0.0.0',
    'category': 'Customer Relationship Management',
    'summary': 'Connect Sale Order with existing Invoice',
    'author': 'LibrERP enterprise network',
    'website': 'https://www.librerp.it',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'sale',
        'account'
    ],
    'data': [
        'wizard/wizard_connect_invoice_view.xml'
    ],
}
