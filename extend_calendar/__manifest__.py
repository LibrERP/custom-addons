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
    'name': "extend_calendar",

    'summary': """
        Calendar extensions for time intervals""",

    'description': """
        Calendar extensions and customizations to manage generic day names with time intervals.
        A time interval expose start and end time as standard time string ("hh:mm") and duration as float.
        A day can contain several time intervals. 
    """,
    #TODO: There isn't a check to avoid partial or total overriding for time intervals in a day.

    'author': "Didotech srl",
    'website': "http://www.didotech.com",
    'category': 'Customization',
    'version': '12.0.0.1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'calendar',
    ],
    "external_dependencies": {
        'python': [
            "workalendar",
        ],
    },

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/hours.xml',
        'data/days.xml',
        'views/days_views.xml',
        'views/intervals_views.xml',
        'views/date_interval_view.xml',
        'views/res_config_settings_views.xml',
        'wizard/calendar_generator.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
