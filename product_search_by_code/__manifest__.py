# © 2023 Marco Tosato - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Search products by code',
    'summary': 'New default search for products: search for products whose default_code starts with the search string',
    'version': '12.0.2.0.1',
    'category': 'Sales',
    'author': 'Didotech SRL',
    'website': 'https://www.didotech.com',
    'development_status': 'Alpha',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'product',
    ],
    'data': [
        'views/product_view.xml'
    ],
}
