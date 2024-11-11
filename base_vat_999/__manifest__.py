# © 2024 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Add 9999x VATs as valid',
    'version': '16.0.0.0',
    'category': 'Accounting/Accounting',
    'summary': """Module adds support for generic 99999x VAT's
        Supported countries:
            - Germany""",
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'base_vat'
    ],
    'data': [],
    'external_dependencies': {
        'python': [
            "stdnum",  # python-stdnum
        ]
    },
}
