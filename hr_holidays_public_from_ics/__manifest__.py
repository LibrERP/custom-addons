# Copyright © 2019-2024 Andrei Levin <andrei.levin@didotech.com>
# Copyright © 2024-2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
# noinspection PyStatementEffect
{
    'name': 'HR Holidays from ics',
    'version': '12.0.0.0.0',
    'category': 'Human Resources',
    'summary': 'Load holidays from URL that points to iCal file (*.ics)',
    'description': """Module adds an URL field and a button inside Public Holidays view:
    
        Leaves -> Public Holidays -> New
    
    Pressing this button will load a calendar from the URL
    
    An example of such URL: 
    
        https://giorni-festivi.eu/ical/italia/2025/
    """,
    'author': 'LibrERP enterprise network',
    'website': 'https://www.librerp.it',
    'development_status': 'Alpha',
    'license': 'AGPL-3',
    'depends': [
        'hr_holidays_public'
    ],
    'external_dependencies': {
        'python': ['vobject']
    },
    'data': ['views/hr_holidays_view.xml'],
    'installable': True,
}
