# © 2024-2025 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Base module to sent/receive xml invoices via SdI',
    'version': '16.0.0.2',
    'category': 'Localization/Italy',
    'summary': 'Base module to sent/receive xml invoices via SdI',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        "l10n_it_fatturapa_out",
        "l10n_it_fatturapa_in",
        "l10n_it_sdi_channel"
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/cron.xml',
        'views/attachment_views.xml',
        'views/partner_views.xml',
        'views/sdi_views.xml',
        'wizard/wizard_import_invoice_view.xml'
    ]
}
