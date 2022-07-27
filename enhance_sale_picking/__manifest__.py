# -*- encoding: utf-8 -*-
##############################################################################
#
#    Created on : 2022-07-07
#    Author : Fabio Colognesi
#    Copyright: Didotech srl 2020 - 2022
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
    'name': "Enhance Sale Order - Picking",

    'summary': """
        Sales Order extensions""",

    'description': """
        Sales extensions adding check on pending stock picking.
        It adivces when choosen partner on Sale Order if any picking is
        ready to be delivered (not yet delivered from other order).
    """,

    'author': "Didotech srl",
    'website': "http://www.didotech.com",
    'category': 'Sales',
    'version': '12.0.1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'sale_stock',
    ],

    # always loaded
    'data': [
        'views/sale_views.xml',
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
