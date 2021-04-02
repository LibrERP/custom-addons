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

from odoo import models, api, fields


class PrintReportLabel(models.TransientModel):
    _name = 'wizard.print.report.label'
    _description = 'Print Report Label'

    _report_type = 'qweb-zpl2'
    
    printer_id = fields.Many2one(
        comodel_name='printing.printer', string='Printer', required=True,
        help='Printer used to print the labels.')
    report_id = fields.Many2one(
        comodel_name='ir.actions.report',
        string='Configured Label',
        required=True,
        domain=lambda self: [
            ('report_type', '=', self._report_type),
            ],
        help='Configured label to print.')
    no_copies = fields.Integer("Copies", required=True, default=1)

    @api.model
    def default_get(self, fields_list):
        values = super(PrintReportLabel, self).default_get(fields_list)

        # Automatically select the printer and label, if only one is available
        printers = self.env['printing.printer'].search(
            [('id', '=', self.env.context.get('printer_zpl2_id'))])
        if not printers:
            printers = self.env['printing.printer'].search([])
        if len(printers) == 1:
            values['printer_id'] = printers.id

        return values

    def print_report(self):
        """
            Prints a selected report, several times as no_copies requires
        """
        counter = 0
        data = {}
        report_model = self.env.context['active_model']
        if report_model == self.report_id.model:
            for item_id in self.env.context['active_ids']:
                content = self.report_id.render_qweb_text([item_id], data=data)[0]
                for counter in range(self.no_copies):
                    counter += 1
                    self.printer_id.print_document(
                        report=None, content=content, doc_format='raw')
