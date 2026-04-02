# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'FatturaPA In Auto',
    'version': '12.0.0.0',
    'category': 'Localization/Italy',
    'summary': 'Automatically create and confirm suppliers invoice',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'l10n_it_fatturapa_in'
    ],
    'data': [
        'data/cron.xml'
    ],
}
