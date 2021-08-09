# -*- encoding: utf-8 -*-
##############################################################################
#
#    Created on : 2021-02-11
#    Author : Fabio Colognesi
#    Copyright: Didotech srl 2020 - 2021
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'extend_calendar',
    'version': '12.0.0.1.0',
    'category': 'Customization',
    'summary': 'Calendar extensions for time intervals',
    'author': 'powERP enterprise network',
    'website': 'https://www.powerp.it',
    'development_status': 'Alpha',
    'license': 'LGPL-3',
    'depends': ['calendar'],
    'external_dependencies': {'python': ['workalendar']},
    'data': [
        'security/ir.model.access.csv',
        'data/hours.xml',
        'data/days.xml',
        'views/days_views.xml',
        'views/intervals_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
