# © 2023 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Sale Order Destination',
    'version': '12.0.0.1',
    'category': 'Customer Relationship Management',
    'summary': 'Add destination address to tree view',
    'author': 'LibrERP enterprise network',
    'website': 'https://www.librerp.it',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'sale',
        'partner_address'
    ],
    'data': [
        'views/sale_order_view.xml'
    ],
}
