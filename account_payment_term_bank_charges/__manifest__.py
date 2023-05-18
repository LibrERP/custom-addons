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
    'name': "Account payment term extension",

    'summary': "Account payment term with bank charges",

    'description': """
        Account payment term with bank charges.
    """,

    'author': "Didotech srl",
    'website': "http://www.didotech.com",
    'category': 'Customization',
    'version': '12.0.2.0.7',
    'depends': [
        'base',
        'account',
        'l10n_it_ddt',
    ],
    'data': [
        "views/account_view.xml",
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
