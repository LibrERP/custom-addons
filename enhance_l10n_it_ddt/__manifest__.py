# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2020-2021 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2021-04-02
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
    'name': "Enhance Transport Document",

    'summary':
    """
        OCA TD extensions
    """,

    'description':
    """
        OCA Transport Document extensions to manage default settings
    """,

    'author': "Didotech srl",
    'website': "http://www.didotech.com",
    'category': 'Stock',
    'version': '12.0.0.2.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'sale',
        'stock',
        'l10n_it_ddt',
        'core_extended',
    ],

    # always loaded
    'data': [
        'views/res_config_settings_views.xml',
        'views/res_partner.xml',
        'views/stock_picking_package_preparation.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'AGPL-3',
}
