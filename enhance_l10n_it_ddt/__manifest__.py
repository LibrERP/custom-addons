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
    'name': 'enhance_l10n_it_ddt',
    'version': '12.0.0.0.1',
    'category': 'Customization',
    'summary': 'OCA ddt extensions and customizations',
    'author': 'powERP enterprise network',
    'website': 'https://www.powerp.it',
    'development_status': 'Alpha',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'sale',
        'stock',
        'l10n_it_ddt',
        'core_extended',
    ],
    'data': [
        'views/res_config_settings_views.xml',
        'views/res_partner.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
