# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Hr Attendance Geolocation Fix',
    'version': '12.0.0.1',
    'category': 'Human Resources',
    'summary': 'Record attendance even when browser geolocation is '
               'denied, unavailable or times out',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'hr_attendance_geolocation',  # OCA/hr
    ],
    'data': [
        'views/assets.xml',
    ],
}
