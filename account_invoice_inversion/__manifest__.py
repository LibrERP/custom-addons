# © 2021 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Account Invoice Inversion',
    'summary': """
    Inverse sign in Account Invoice and transform it in Credit Note""",
    'description': """
    Inverse sign in Account Invoice and transform it in Credit Note
""",
    'version': '12.0.2.0',
    'category': 'Accounting',
    'author': 'Didotech Srl',
    'website': 'https://github.com/LibrERP/custom-addons',
    'depends': [
        'base',
        # 'mail',
        'account'
    ],
    'data': [
        'views/account_invoice_view.xml'
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    "external_dependencies": {}
}
