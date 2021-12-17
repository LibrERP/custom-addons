# Copyright 2019 ForgeFlow, S.L.
# Copyright 2020 CorporateHub (https://corporatehub.eu)
# © 2021 Didotech  (https://www.didotech.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Account Bank Statement Import TXT/CSV/XLSX",
    "summary": "Import TXT/CSV or XLSX files as Bank Statements in Odoo",
    "version": "12.0.2.0.5_9",
    "category": "Accounting",
    "website": "https://github.com/LibrERP/custom-addons",
    "author": "ForgeFlow, " "CorporateHub, " "Odoo Community Association (OCA)",
    "maintainers": ["didotech srl"],
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account_bank_statement_import",
        "multi_step_wizard",
        "web_widget_dropdown_dynamic",
    ],
    "external_dependencies": {
        "python": [
            "xlrd",
            'openpyxl',
        ]
    },
    'excludes': ['account_bank_statement_import_txt_xlsx'],
    "data": [
        "security/ir.model.access.csv",
        "data/map_data.xml",
        "views/account_bank_statement_import_sheet_mapping.xml",
        "views/account_bank_statement_import.xml",
        "views/account_journal_views.xml",
        "wizards/account_bank_statement_import_sheet_mapping_wizard.xml",
    ],
}
