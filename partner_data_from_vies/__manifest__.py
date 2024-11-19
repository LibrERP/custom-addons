# ©  2020-2021 Didotech srl
# © 2024 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Automatic partner creation based on VAT number',
    'version': '16.0.1.4.1',
    'category': 'Customer Relationship Management',
    'summary': 'Using VIES webservice, name and address information will be fetched and added to the partner.',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'external_dependencies': {
        'python': [
            'requests',
            'BeautifulSoup4',
        ]
    },
}
