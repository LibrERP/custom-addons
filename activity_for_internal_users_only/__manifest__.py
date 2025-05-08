# © 2025 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Activity for internal users only',
    'version': '16.0.0.0',
    'category': 'Tools',
    'summary': 'Assign activity only to internal users',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'mail'
    ],
    'data': [
        'views/mail_activity_views.xml'
    ],
}
