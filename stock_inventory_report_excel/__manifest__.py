# © 2024 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Stock Inventory Report Excel',
    'version': '12.0.0.0',
    'category': 'stock',
    'summary': 'Download Inventory data as Excel file',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'stock'
    ],
    'data': [
        'views/stock_inventory_views.xml',
        'wizard/wizard_inventory_report.xml'
    ],
    "external_dependencies": {
        'python': [
            "openpyxl",
        ],
    },
}
