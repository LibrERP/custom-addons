# © 2022 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Partner history",
    # "summary":
    #     "Module to make the VAT number unique for customers and suppliers.",
    "version": "12.0.0.0.1",
    "category": "Customer Relationship Management",
    "website": "https://github.com/LibrERP/custom-addons",
    "author": "Didotech srl, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["base"],
    'data': [
        'views/partner_view.xml',
    ],
    'excludes': ['partner_vat_unique'],
    "installable": True,
    "application": True,
}
