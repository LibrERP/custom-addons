# -*- encoding: utf-8 -*-
##############################################################################
#
#    LibrERP, Open Source Product Enterprise Management System    
#    Copyright (C) 2020-2023 Didotech srl (<http://didotech.com>). All Rights Reserved
#
#    Created on : 2023-03-26
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
    'name': "Enhance Manufacturing",

    'summary': """
        Manufacturing extensions""",

    'description': """
        Manufacturing extensions adding fixes and improvements.
    """,

    'author': "Didotech srl",
    'website': "http://www.didotech.com",
    'category': 'Manufacturing',
    'version': '12.0.0.4.0',

    # any module necessary for this one to work correctly
    'depends': [
        'mrp',
    ],

    # always loaded
    'data': [
        'data/scheduled_action.xml',
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
