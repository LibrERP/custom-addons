# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Contract Sale Generation Plus',
    'version': '18.0.1.0',
    'category': 'Contract Management',
    'summary': """Module correct some problems of the module Contract Sale Generation:
        - Copy values of Analytic Distribution
        - Copy values of period start and end into invoice
        - Adds contract_ids field
        - Set constraint to forbid creating contracts without recurring interval
    """,
    'author': 'Codebeex srl',
    'website': 'https://github.com/LibrERP/custom-addons',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'contract_sale_generation',  # OCA/contract
        'sale_start_end_dates',  # OCA/sale-workflow
    ],
    'data': [
        'views/sale_order_views.xml',
    ],
}
