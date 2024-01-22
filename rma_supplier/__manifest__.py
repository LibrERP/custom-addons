# © 2024 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'RMA Supplier',
    'version': '12.0.0.1',
    'category': 'RMA',
    'summary': 'Add Supplier to the RMA module',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'rma'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/inventory_state.xml',
        'views/rma_views.xml'
    ],
}
