# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2012 Andrea Cometa All Rights Reserved.
#                       www.andreacometa.it
#                       openerp@andreacometa.it
#    Copyright (c) 2020 Michele Trevisan <michele.trevisan@didotech.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Sequence Recovery',
    'version': '0.0.1',
    'category': 'Sequences',
    'description':
        """
        [ENG] Is useful for sequences recovery eg from a deleted invoice.
        [ITA] Modulo per la gestione del recupero dei buchi delle sequence (DDT, Fatture, etc.)
        È sufficente ereditare l'unlink di una classe con sequence per ottenere la funzionalità di ripristino
        """,
    'author': 'Andrea Cometa, Didotech SRL',
    'website': 'http://www.andreacometa.it',
    'license': 'AGPL-3',
    "active": False,
    "installable": True,
    "depends": ['base'],
    "update_xml": [
        'security/sequence_recovery_security.xml',
        'security/ir.model.access.csv',
        'views/sequence_view.xml',
    ],
}
