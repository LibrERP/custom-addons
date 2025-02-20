# © 2025 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Account Payment Invoice',
    'version': '12.0.0.0',
    'category': 'Banking addons',
    'summary': """Module automatically sets partner_bank_id in Invoice
    Attention! Module is incompatible with account_banking_sepa_direct_debit module""",
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account_payment_partner',
    ],
    'data': [],
}
