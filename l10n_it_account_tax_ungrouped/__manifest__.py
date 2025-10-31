# © 2025 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'No Tax Grouping',
    'version': '18.0.0.0',
    'category': 'Accounting/Localizations/EDI',
    'summary': 'Module removes the tax grouping not required in Italy',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account'
    ],
    'data': [
        'report/report_invoice.xml'
    ],
}
