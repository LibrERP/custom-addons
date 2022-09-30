# © 2022 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
{
    'name': 'CIG and CUP in Sale Order',
    'version': '12.0.0.1',
    'category': 'Accounting',
    'summary': "Automatically add CIG and CUP if they are present in partner's shipping address",
    'author': 'SHS-AV s.r.l.',
    'website': 'https://www.didotech.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'sale',
        'l10n_it_fatturapa_sale'
    ],
    'external_dependencies': {},
    'data': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
