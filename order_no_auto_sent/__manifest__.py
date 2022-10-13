# © 2022 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
{
    'name': "Sale and Purchase Order no auto Quotation Sent",
    'summary': """
        Don't automatically change order state in 'Quotation Sent' after printing""",
    'author': "LibrERP enterprise network",
    'website': "https://github.com/LibrERP/custom-addons",
    'category': 'Sales',
    'version': '12.0.0.1',
    'depends': [
        'base',
        'sale',
    ],
    # always loaded
    'data': [],
    # only loaded in demonstration mode
    'demo': [],
}
