# © 2022 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
{
    'name': "Sale Order Partner",
    'summary': """
        Limit Shipping and Invoice addresses to addresses that has partner as parent""",
    'author': "LibrERP enterprise network",
    'website': "https://github.com/LibrERP/custom-addons",
    'category': 'Sales',
    'version': '12.0.0.0',
    'depends': [
        'base',
        'sale'
    ],
    'data': [
        'views/sale_order_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
}
