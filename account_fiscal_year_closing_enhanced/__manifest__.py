# © 2022 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Account Fiscal Year Closing Enhanced',
    'version': '12.0.0.0',
    'category': 'Accounting',
    'summary': (
        'Allow account move lines to be registered without partners when closing accounts at the end of a fiscal year'
    ),
    'author': 'LibrERP',
    'website': 'https://www.didotech.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'l10n_it_validations',
        'account_fiscal_year_closing',
    ],
    'data': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
