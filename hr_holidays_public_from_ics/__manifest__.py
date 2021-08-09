# Copyright © 2019 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'HR Holidays from ics',
    'version': '12.0.0.0.0',
    'category': 'Human Resources',
    'summary': 'Load holidays from URL that points to iCal file (*.ics)',
    'author': 'powERP enterprise network',
    'website': 'https://www.powerp.it',
    'development_status': 'Alpha',
    'license': 'AGPL-3',
    'depends': ['hr_holidays_public'],
    'external_dependencies': {'python': ['vobject']},
    'data': ['views/hr_holidays_view.xml'],
    'installable': True,
}
