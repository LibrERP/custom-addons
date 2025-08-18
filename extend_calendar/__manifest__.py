# -*- encoding: utf-8 -*-
##############################################################################
#
#    Oddo Addons Module, Open Source   
#    Copyright (C) 2025 Codebeex srl (<http://www.codebeex.com>). All Rights Reserved
#
#    Created on: 2025-08-14
#    Author : Fabio Colognesi
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
    'name': "Extend Calendar",

    'summary': """
        Calendar extensions for time intervals""",

    'description': """
        Calendar extensions to manage working days for partners, considering current or specific year.
        Introduces standardized generic weeks and days with time intervals.
        A time interval exposes start and end time as standard time string ("hh:mm") and duration as float.
        A day can contain several time intervals. Functions help to evaluate duration on intervals.
    """,
    #TODO: There isn't a check to avoid partial or total overriding for time intervals in a day.

    'author': "Codebeex srl",
    'website': "http://www.codebeex.com",
    'category': 'Time Management',
    'version': '18.0.0.0',

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
        'data/weeks.xml',
        'views/weeks_views.xml',
        'views/days_views.xml',
        'views/intervals_views.xml',
        'views/res_config_settings_views.xml',
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
