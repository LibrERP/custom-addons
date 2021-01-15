# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2020-2021 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2021-01-15
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

from odoo  import _, models, api


class PackingListReport(models.AbstractModel):
    _template='packing_list.report_packing_list'
    _name = "report.%s" %(_template)
    _description = "Packing List"
    
    @api.model
    def _get_report_values(self, docids, data=None):
        return {'docs': self.env['stock.picking'].browse(docids)}

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['stock.picking']
        report = report_obj._get_report_from_name(self._template)
        docargs = {
            'doc_ids': docids,
            'doc_model': 'mrp.bom',
            'docs': self,
            'data': data,
        }
        return self.env['report'].render(self._template, docargs)
