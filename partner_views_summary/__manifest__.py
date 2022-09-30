##############################################################################
#
#    Copyright (C) 2020-2022 Didotech srl
#    (<http://www.didotech.com/>).
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
    'name': "Partner Common Summary",

    'summary': "Partner payments summary",

    'description': """
        Extends Partner entities and views.
    """,

    'author': "Didotech srl",
    'website': "http://www.didotech.com",
    'category': 'Customization',
    'version': '12.0.1.0.0',
    'depends': [
        'base',
    ],
    'data': [
        "views/res_partner.xml",
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
