# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Address required fields',
    'version': '16.0.0.0',
    'category': 'Generic Modules/Base',
    'summary': """Module set as required fields for the main partner:
        - street,
        - city,
        - state,
        - cap,
        - mobile,
        
        if partner is a company:
        - vat
        else:
        - fiscalcode
    """,
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'l10n_it_fiscalcode'
    ],
    'data': [
        'views/res_partner_views.xml'
    ],
}
