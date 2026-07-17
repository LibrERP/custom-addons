# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Time Off Weekend Included',
    'version': '18.0.1.0',
    'category': 'Human Resources/Time Off',
    'summary': 'Count weekend days in the leave duration for leave types such '
               'as marriage leave, where the legal duration is expressed in '
               'calendar days rather than working days.',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'hr_holidays',
    ],
    'data': [
        'views/hr_leave_type_views.xml',
    ],
    'post_init_hook': 'post_init_hook',
}
