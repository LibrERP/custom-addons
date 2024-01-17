# © 2024 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'RMA Stage',
    'version': '12.0.0.0',
    'category': 'RMA',
    'summary': 'Module adds configurable stages to RMA',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'web',
        'rma'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/rma_assets.xml',
        'views/rma_views.xml'
    ],
}
