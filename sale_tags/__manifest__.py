#    Copyright (C) 2020-2023 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2021-07-05
#    Author : Fabio Colognesi
#
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
    'name': "Sale Tags",

    'summary': """
        Tagging Sale Orders""",

    'description': """
        Adding tag to Sale Orders to manage filters on deliveries and invoices.
        To help understanting if a Sale Order can be closed or it needs to be
        followed up by sale team.
    """,

    'author': "Didotech srl",
    'website': "http://www.didotech.com",
    'category': 'Sales',
    'version': '12.0.0.3.4',

    # any module necessary for this one to work correctly
    'depends': [
        'sale',
        'sale_stock',
    ],

    # always loaded
    'data': [
        'data/scheduled_action.xml',
        'views/sale_view.xml',
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
