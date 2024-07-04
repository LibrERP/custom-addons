# © 2024 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Contract generic names',
    'version': '16.0.0.0',
    'category': "Contract Management",
    'summary': 'Make contract module more generic and not tied to invoice',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'contract'  # OCA/contract
    ],
    'data': [
        'views/contract_views.xml'
    ],
}
