# © 2021 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': "Invoice line editing form",

    'summary': """
        Invoice line editing form""",

    'description': """
        Module permits to edit invoice line in a separate form and not inside the table
    """,

    'author': "Powerp",
    'website': "https://www.powerp.it",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.0.0',
    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'account'
    ],
    # always loaded
    'data': [
        'views/account_invoice_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [],
}
