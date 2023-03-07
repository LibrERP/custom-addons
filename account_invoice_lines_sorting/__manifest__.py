#    Copyright (C) 2023 Didotech srl (<https://www.didotech.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "Invoice Line Sorting",
    'summary': """
        Sort invoice line according sale order line sequence""",
    'author': "Didotech s.r.l.",
    'website': "https://github.com/LibrERP/custom-addons",
    'category': 'Accounting',
    'version': '12.0.1.0.1',
    'depends': [
        'base',
        'account',
        'sale',
        # 'stock',
        # 'l10n_it_ddt',
        # 'enhance_l10n_it_ddt',
    ],
    'data': [
        'views/account_invoice_view.xml',
    ],
}
