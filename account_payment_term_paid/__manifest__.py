# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Account Payment Term Already Paid',
    'version': '16.0.0.0',
    'category': 'Accounting',
    'summary': 'Flag a payment term as already paid; invoices using it skip payment info',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'views/account_payment_term_views.xml',
    ],
}
