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
    'name': 'extend_report',
    'version': '12.0.0.5.0',
    'category': 'Customization',
    'summary': 'Report extensions and customizations',
    'author': 'powERP enterprise network',
    'website': 'https://www.powerp.it',
    'development_status': 'Alpha',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'product',
        'mrp',
        'stock',
        'base_report_to_printer',
    ],
    'data': [
        'wizard/print_report_label.xml',
        'views/action_report.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
