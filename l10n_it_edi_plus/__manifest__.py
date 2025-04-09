# © 2025 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'More functionality for FatturaPA',
    'version': '18.0.0.0',
    'category': 'Accounting/Localizations/EDI',
    'summary': 'More functionality for FatturaPA',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account',
        'l10n_it_edi'
    ],
    'data': [
        'data/invoice_it_template.xml',
        'views/account_views.xml',
        'views/partner_views.xml'
    ],
}
