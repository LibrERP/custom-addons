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

from odoo import models, fields, api, _

class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    report_type = fields.Selection(
        selection_add=[('qweb-zpl2', 'ZPL2 - Zebra Printers')]
    )

    @api.model
    def render_qweb_zpl2(self, res_ids=None, data=None):
        """
            Queue to a zebra printer a text flow as built
             in report definition.
            It works with only one Zebra printer.
        """
        document, doc_format = self.render_qweb_text(res_ids, data=data)

        behaviour = self.behaviour()
        printer = behaviour.pop('printer', None)
        can_print_report = self._can_print_report(behaviour, printer, document)

        if can_print_report:
            printer.print_document(self, document, doc_format='raw',
                                   **behaviour)
        return document, doc_format

