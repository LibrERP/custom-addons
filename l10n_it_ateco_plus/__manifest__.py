# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'ITA - Codici Ateco Update',
    'version': '18.0.0.1',
    'category': 'Localization/Italy',
    'summary': """This module extends functionality of l10n_it_ateco module
    and adds 2025 classification data""",
    'author': 'Codebeex srl',
    'website': 'https://github.com/librerp/custom-addons',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'l10n_it_ateco'
    ],
    'data': [
        'data/ateco_data_2025.xml',
        'views/ateco_views.xml'
    ],
}
