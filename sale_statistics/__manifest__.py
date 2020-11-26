# -*- encoding: utf-8 -*-
############################################################################
#
#    Copyright (C) 2020-2020 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2020-11-26
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
############################################################################
{
    'name': 'Sale Statistics',
    'version': '12.0.0.0',
    "author": "Didotech srl",
    'category': 'Sales Analisys',
    'description': """
Sales Statistics
================

Sales Statistics module that covers:
------------------------------------
    * Sale Orders
    * Purchase Orders
    * Sale Volumes

Creates a dashboard for accountants that includes:
--------------------------------------------------
    * Sales organized by Year, Quarter, Month, Week
    * Sales grouped by Supplier
    * Sales grouped by Salesman
    * Sales grouped by Customer
    * Sales grouped by Product Template
    * Sales grouped by Product

Authors:
--------
    * Didotech srl

Contributors:
-------------
    * Fabio Colognesi

    """,
    'website': 'http://www.didotech.com',
    'depends': [
        'sale',
    ],
    'data': [
        'data/res_country_data.xml',
        'security/account_security.xml',
        'security/ir.model.access.csv',
        'report/sale_report_view.xml',
        'data/scheduled_action.xml',
        'views/board_view.xml',
    ],
    'qweb': [
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
