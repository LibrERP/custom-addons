# Author: Damien Crier
# Author: Julien Coux
# Copyright 2016 Camptocamp SA
# Copyright 2023  Didotech s.r.l
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Account Financial Reports Extended aged partner balance',
    'version': '12.0.1.0.0',
    'category': 'Reporting',
    'summary': 'OCA Financial Reports extension',
    'author': 'Didotech s.r.l.',
    "website": "https://www.didotech.com/",
    'depends': [
        'account',
        'date_range',
        'report_xlsx',
        'account_financial_report',
    ],
    'data': [
        'wizard/aged_partner_balance_wizard_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'AGPL-3',
}
