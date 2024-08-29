# © 2024 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Mass Mailing PEC',
    'version': '16.0.0.0',
    'category': 'Marketing/Email Marketing',
    'summary': 'Add PEC functionality to mass mailing module',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'mass_mailing',
        'mass_mailing_event'
    ],
    'data': [
        'views/ir_mail_server_views.xml',
        'views/mass_mailing_views.xml',
        'views/res_config_settings_views.xml'
    ],
}
