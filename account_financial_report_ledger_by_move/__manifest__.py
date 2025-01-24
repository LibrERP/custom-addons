# Author: Didotech s.r.l.
# Copyright 2023 Didotech.com https://www.didotech.com
# Copyright 2025 Codebeex srl https://www.codebeex.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Account Financial Reports General Ledger By Move',
    'version': '12.0.1.0.3',
    'category': 'Reporting',
    'summary': 'Financial Reports extensions',
    'author': 'Didotech s.r.l.',
    "website": "https://www.codebeex.com",
    'depends': [
        'account',
        'date_range',
        'report_xlsx',
        'account_financial_report',
    ],
    'data': [
        'wizard/general_ledger_wizard_view.xml',
        'report/templates/general_ledger.xml',
        'views/report_general_ledger.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
