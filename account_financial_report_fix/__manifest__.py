# © 2024 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Fix Account Financial Report',
    'version': '12.0.0.0',
    'category': 'Reporting',
    'summary': 'Fix Account Financial Report template name problems',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account_financial_report'
    ],
    'data': [
        'report/templates/reports.xml'
    ],
}
