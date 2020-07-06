#  Copyright 2011-2012 Domsense s.r.l. (<http://www.domsense.com>)
#  Copyright 2012-17 Agile Business Group (<http://www.agilebg.com>)
#  Copyright 2012-15 LinkIt Spa (<http://http://www.linkgroup.it>)
#  Copyright 2015 Associazione Odoo Italia (<http://www.odoo-italia.org>)
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'ITA - Liquidazione IVA',
    'summary': 'Versamento Iva periodica (mensile o trimestrale) ',
    'version': '12.0.1.5.3',
    'category': 'Localization/Italy',
    'author': 'Odoo Community Association (OCA) and other subjects',
    'website': 'https://odoo-community.org/',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'account_tax_balance',
        'date_range',
        'l10n_it_account',
        'l10n_it_fiscalcode',
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
    'development_status': 'Beta',
}
