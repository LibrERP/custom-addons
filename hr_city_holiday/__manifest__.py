# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'HR City Holiday',
    'version': '12.0.0.0',
    'category': 'Human Resources',
    'summary': 'Module permits to define a public holiday for an address',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'hr',
        'hr_holidays_public'  # OCA/hr
    ],
    'data': [
        'data/hr_city_holidays.xml',
        'views/hr_holidays_public_views.xml',
        'views/partner_views.xml'
    ],
}
