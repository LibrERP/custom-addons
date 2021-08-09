# Copyright 2019 ForgeFlow, S.L.
# Copyright 2020 CorporateHub (https://corporatehub.eu)
# © 2021 Didotech  (http://www.didotech.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Account Bank Statement Import TXT/CSV/XLSX',
    'version': '12.0.2.0.5_a',
    'category': 'Accounting',
    'summary': 'Import TXT/CSV or XLSX files as Bank Statements in Odoo',
    'author': 'powERP enterprise network, `CorporateHub',
    'website': 'https://www.powerp.it',
    'development_status': 'Alpha',
    'license': 'AGPL-3',
    'depends': [
        'account_bank_statement_import',
        'multi_step_wizard',
        'web_widget_dropdown_dynamic',
    ],
    'external_dependencies': {'python': ['xlrd']},
    'data': [
        'security/ir.model.access.csv',
        'data/map_data.xml',
        'views/account_bank_statement_import_sheet_mapping.xml',
        'views/account_bank_statement_import.xml',
        'views/account_journal_views.xml',
        'wizards/account_bank_statement_import_sheet_mapping_wizard.xml',
    ],
    'installable': True,
    'maintainers': ['alexey-pelykh'],
}
