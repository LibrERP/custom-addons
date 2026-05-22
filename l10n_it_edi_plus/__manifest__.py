# © 2025-2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'More functionality for FatturaPA',
    'version': '18.0.0.2',
    'category': 'Accounting/Localizations/EDI',
    'summary': 'Module adds more fields used in FatturaPA',
    'description': """
FatturaPA Fields Extension
==========================

Module adds more fields used in FatturaPA:

- 2.1.1.11   Causale
- 1.2.6      RiferimentoAmministrazione
- 2.2.1.15   RiferimentoAmministrazione
- 2.2.1.16.1 TipoDato
- 2.2.1.16.2 RiferimentoTesto

Filter to see only rejected invoices
    """,
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
