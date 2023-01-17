# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2020-2021 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2021-00-11
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
    'name': "Enhance Stock Picking",

    'summary': 
        """
            Stock picking extensions
        """,

    'description': 
        """
            Stock picking extensions referring to TD.
        """,

    'author': "Didotech srl",
    'website': "http://www.didotech.com",
    'category': 'Stock',
    'version': '12.0.0.4.0',

    # any module necessary for this one to work correctly
    'depends': [
       'stock',
       'l10n_it_ddt',  # OCA l10n_italy
    ],

    # always loaded
    'data': [
        'data/scheduled_action.xml',
        'views/stock_picking_views.xml',
        'wizard/picking_edit_lines_wizard.xml'
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
