# © 2025 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Account Move Is Sent',
    'version': '18.0.0.1',
    'category': 'Accounting/Localizations/EDI',
    'summary': 'Give a possibility to set an Invoice as sent or as not sent in case there is no transaction ID',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account',
        'l10n_it_edi'
    ],
    'data': [
        'views/account_move_views.xml'
    ],
}
