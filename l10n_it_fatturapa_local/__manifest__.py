# © 2024 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Export Fatturapa in local folder ',
    'version': '16.0.0.0',
    'category': 'Localization/Italy',
    'summary': 'Export Fatturapa in local folder',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        "l10n_it_fatturapa_out",
        # "l10n_it_fatturapa_in",
        "l10n_it_sdi_channel"
    ],
    'data': [
        'views/sdi_views.xml',
        "data/sdi_channel.xml",
    ],
}
