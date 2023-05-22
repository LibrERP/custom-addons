##############################################################################
#
#    Copyright (C) 2022-2023 Didotech SRL
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
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
    'name': "Feature for invoice generation from Transport Documents",

    'summary': """
         Wizard which handles invoices and credite notes. """,

    'description': """
        Wizard which handles invoices and credite notes.
    """,

    'author': "Didotech srl",
    'website': "http://www.didotech.com",
    'category': 'Customization',
    'version': '12.0.3.1.6',

    'depends': [
        'base',
        'stock',
        'l10n_it_ddt',
        'l10n_it_ddt_invoice_extension',
        'account_invoice_from_stock_picking',
        'queue_job',

    ],

    'data': [
        'wizard/wizard_invoice_from_ddt.xml',
        'views/stock_picking_view.xml',
        'views/menuitem.xml',
        'views/res_config.xml',
        'wizard/wizard_credit_note_from_picking.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'AGPL-3',
}
