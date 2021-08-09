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
    'name': 'enhance_purchase',
    'version': '12.0.0.0.1',
    'category': 'Customization',
    'summary': 'Purchase extensions and customizations',
    'author': 'SHS-AV s.r.l.',
    'website': 'https://www.zeroincombenze.it',
    'development_status': 'Alpha',
    'license': 'LGPL-3',
    'depends': ['purchase'],
    'data': ['views/purchase_views.xml'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
