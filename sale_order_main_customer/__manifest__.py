# © 2022 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
{
    'name': "Sale Order Main Customer",
    'summary': """
        Exclude contacts from main addresses""",
    'author': "LibrERP enterprise network",
    'website': "https://github.com/LibrERP/custom-addons",
    'category': 'Sales',
    'version': '12.0.0.0',
    'depends': [
        'base',
        'sale',
        'base_view_inheritance_extension',  # OCA: server-tools
    ],
    'data': [
        'views/sale_order_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
}
