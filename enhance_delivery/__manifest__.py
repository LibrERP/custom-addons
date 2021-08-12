# -*- encoding: utf-8 -*-
##############################################################################
#
#    LibrERP, Open Source Product Enterprise Management System    
#    Copyright (C) 2020-2021 Didotech srl (<http://didotech.com>). All Rights Reserved
#
#    Created on : 2021-08-12
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
    'name': "Enhance Delivery Costs",

    'summary': """
        Delivery Costs extensions""",

    'description': """
        Delivery Costs extensions adding Price Ranges to quote shipping.
    """,

    'author': "Didotech srl",
    'website': "http://www.didotech.com",
    'category': 'Stock',
    'version': '12.0.0.0.0',

    # any module necessary for this one to work correctly
    'depends': [
        'delivery',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/delivery_carrier_views.xml'
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
