# -*- encoding: utf-8 -*-
##############################################################################
#
#    Oddo Addons Module, Open Source   
#    Copyright (C) 2024-2025 Codebeex srl (<http://www.codebeex.com>). All Rights Reserved
#
#    Created on: 2025-03-17
#    Author : odoo
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
    'name': "MRP MPS Customizations",

    'summary': "Customization: Riesco - MRP MPS Customization",

    'description': """
        Extends Mrp Production Schedule entities and views.
    """,

    'author': "Codebeex srl",
    'website': "http://www.codebeex.com",
    'category': 'Customization',
    'version': '18.0.0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'mrp_mps',
    ],

    # always loaded
    'data': [
        'views/mrp_mps_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}

