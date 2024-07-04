# © 2022-2023 Andrei Levin <andrei.levin@didotech.com>
# © 2024 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
# noinspection PyStatementEffect
{
    'name': "Sale Order Partner",
    'summary': """
        Limit Shipping and Invoice addresses to addresses that has partner as parent""",
    'author': "Codebeex",
    'website': "https://github.com/LibrERP/custom-addons",
    'category': 'Sales',
    'version': '16.0.0.1',
    'depends': [
        'base',
        'sale'
    ],
    'data': [
        'views/sale_order_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    'test': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
