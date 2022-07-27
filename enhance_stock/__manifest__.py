# -*- encoding: utf-8 -*-
##############################################################################
#
#    Created on : 2022-07-27
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
    'name': "Enhance Stock",

    'summary': """
        Stock extensions""",

    'description': """
        Extends Stock entity adding action to show products
         contained into current location.
    """,

    'author': "Didotech srl",
    'website': "http://www.didotech.com",
    'category': 'Stock',
    'version': '12.0.0.0',

    'depends': [
        'product',
        'stock',
    ],

    'data': [
        'views/stock_location_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'AGPL-3',
}
