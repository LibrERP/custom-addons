# © 2021 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'l10n_it_fatturapa_improved',
    'summary': """
    Corrections to official l10n_it_fatturapa""",
    'description': """
    Copy related document for each line when creating invoice from TD
""",
    'version': '12.0.0.0',
    'category': 'Accounting',
    'author': 'Didotech Srl',
    'website': 'https://github.com/LibrERP/custom-addons',
    'depends': [
        'base',
        'account',
        'l10n_it_ddt'
    ],
    'data': [],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    "external_dependencies": {}
}
