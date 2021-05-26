# © 2021 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'l10n_it_ddt_detach',
    'summary': """
    Detach Invoice from TD""",
    'description': """
    Detach Invoice from TD to be able to create new Invoice. 
    Operation is required when wrong invoice was created and already send to SDI and new Invoice should be created
""",
    'version': '12.0.0.1',
    'category': 'Accounting',
    'author': 'Didotech Srl',
    'website': 'https://github.com/LibrERP/custom-addons',
    'depends': [
        'base',
        'account',
        'l10n_it_ddt'
    ],
    'data': [
        'wizard/wizard_detach_invoice_view.xml',
        'views/stock_picking_package_preparation_view.xml'
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    "external_dependencies": {}
}
