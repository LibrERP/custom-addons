# Copyright 2011-12 Domsense s.r.l. <http://www.domsense.com>
# Copyright 2012-17 Agile Business Group <http://www.agilebg.com>
# Copyright 2012-15 LinkIt Spa <http://http://www.linkgroup.it>
# Copyright 2015 Associazione Odoo Italia <http://www.odoo-italia.org>
# Copyright 2020 Odoo Community Association (OCA) <https://odoo-community.org>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'ITA - Liquidazione IVA',
    'version': '12.0.1.5.3',
    'category': 'Localization/Italy',
    'summary': 'Allow to create the "VAT Statement".',
    'author': 'Odoo Community Association (OCA) and other partners',
    'website': 'https://odoo-community.org',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'account_tax_balance',
        'date_range',
        'l10n_it_account',
        'l10n_it_fiscalcode',
        'l10n_it_account_tax_kind',
        'web',
    ],
    'data': [
        'wizard/add_period.xml',
        'wizard/remove_period.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'report/reports.xml',
        'views/report_vatperiodendstatement.xml',
        'views/config.xml',
        'views/account_view.xml',
    ],
    'installable': True,
}
