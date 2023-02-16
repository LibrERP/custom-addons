# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2023 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2023-01-17
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
    'name': 'Italian Localization - FatturaPA - Emission',
    'version': '12.1.0.3.0',
    'category': 'Localization/Italy',
    'summary': 'Electronic invoices emission',
    'author': 'Didotech SRL',
    'description': """

Italian Localization - FatturaPA - Emission
===========================================

""",
    'website': 'http://www.didotech.com',
    'license': 'AGPL-3',
    "depends": [
        'l10n_it_fatturapa',
        'l10n_it_fatturapa_out',
    ],
    "data": [
        'views/company_view.xml',
        'wizard/wizard_export_fatturapa_view.xml',
    ],
    "installable": True
}
