# © 2024 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
#
# README.rst generation:
# cd custom-addons
# oca-gen-addon-readme --repo-name=custom-addons --branch=16.0 --addon-dir=mass_mailing_pec --org-name=LibrERP
{
    'name': 'Mass Mailing PEC',
    'version': '16.0.0.1',
    'category': 'Marketing/Email Marketing',
    'summary': 'Add PEC functionality to mass mailing module',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'mass_mailing',
        'mass_mailing_event',
        # 'l10n_it'
    ],
    'data': [
        'views/fetchmail_views.xml',
        'views/ir_mail_server_views.xml',
        'views/mailing_mailing_views.xml',
        'views/mailing_trace_views.xml',
        'views/mass_mailing_views.xml',
        'views/res_config_settings_views.xml'
    ],
    'external_dependencies': {
        'python': [
            'mail-parser'
        ],  # pip install mail-parser
    }
}
