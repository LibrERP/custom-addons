# -*- encoding: utf-8 -*-
##############################################################################
#
#    Created on : 2021-05-14
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
    'name': "l10n_it_ddt_improved",

    'summary': """
        OCA ddt extension for packaging""",

    'description': """
        OCA ddt extensions to compose product packaging in an automatic way
    """,

    'author': "Didotech srl",
    'website': "http://www.didotech.com",
    'category': 'Customization',
    'version': '12.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': [
        'l10n_it_ddt',
        'core_extended',
        'delivery',
        'stock',
        'extend_report',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/decimal_precision.xml',
        'report/report_package_barcode.xml',
        'report/format_package_barcode.xml',
        'views/product_packaging_view.xml',
        'views/stock_picking_package_preparation.xml',
        'views/stock_quant_views.xml',
        'views/product_views.xml',
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
