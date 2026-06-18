# © 2022-2023 Andrei Levin <andrei.levin@didotech.com>
# © 2024-2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    "name": "Partner history",
    # "summary":
    #     "Module to make the VAT number unique for customers and suppliers.",
    "version": "12.0.0.0.2",
    "category": "Customer Relationship Management",
    "website": "https://github.com/LibrERP/custom-addons",
    "author": "Didotech srl, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "base"
    ],
    'data': [
        'views/partner_view.xml',
    ],
    'excludes': [
        'partner_vat_unique'
    ],
    "installable": True,
    "application": True,
}
