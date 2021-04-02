# -*- encoding: utf-8 -*-
##############################################################################
#
#    (<http://www.didotech.com/>).
#
#    Created on : 2021-01-22
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
    'name': "extend_report",

    'summary': """
        Report extensions and customizations""",

    'description': """
        Report extensions and customizations to manage Zebra printing
        Managing "zpl2" report types.
    """,

    'author': "Didotech srl",
    'website': "http://www.didotech.com",
    'category': 'Customization',
    'version': '12.0.0.3.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'product',
        'mrp',
        'stock',
        'base_report_to_printer',
    ],

    # always loaded
    'data': [
        'wizard/print_report_label.xml',
        'views/action_report.xml',
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
