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
    'version': '12.0.6.0',
    'category': 'Business Analisys',
    'author': 'powERP enterprise network',
    'website': 'https://www.powerp.it',
    'development_status': 'Alpha',
    'license': 'LGPL-3',
    'depends': ['sale', 'sale_stock', 'sale_margin'],
    'data': [
        'security/sale_statistics.xml',
        'security/account_security.xml',
        'security/ir.model.access.csv',
        'data/res_country_data.xml',
        'data/res.country.region.csv',
        'data/res.country.state.csv',
        'report/sale_report_view.xml',
        'data/scheduled_action.xml',
        'views/board_view.xml',
        'views/partner_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
