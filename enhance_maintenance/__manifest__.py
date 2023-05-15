# -*- encoding: utf-8 -*-
##############################################################################
#
#    LibrERP, Open Source Product Enterprise Management System    
#    Copyright (C) 2020-2023 Didotech srl (<http://didotech.com>). All Rights Reserved
#
#    Created on : 2023-03-24
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
    'name': 'Maintenance Enhancement',
    'version': '12.0.1.0',
    'author': 'Didotech srl',
    'website': 'http://www.didotech.com',
    'support': 'support@didotech.com',
    'category': 'Human Resources',
    'sequence': 10,
    'summary': 'Maintenance Equipment & Request Enhanced',
    'images': [],
    'depends': [
        'product',
        'sale_management',
        'analytic',
        'maintenance',
        'hr_expense',
        'hr_timesheet',
        'sale_expense',
        ],
    'description':
    """
        Extends Maintenance Equipment and Request.
        Allows to register time sheets for people that executes maintenance.
        Allows to register spare part products consumed to apply maintenance.
        Allows to register purchased products to ensure maintenance.
        Allows to register expenses sustained to execute maintenance.
        Send all invoiceable to Sale Order managing operations in standard flow.
        Allows to manage one or more Sale Orders.
        Allows to register all invoices related to Maintenance Request.
    """,
    'init_xml': [
        ],
    'data': [
        'data/uom_data.xml',
        'data/product_data.xml',
        'security/ir.model.access.csv',
        'views/res_config_view.xml',
        'views/maintenance_views.xml',
       ],
    'demo_xml': [
        ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'active': False,
    'license': 'LGPL-3',
}
