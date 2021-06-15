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

from odoo import models, fields, api
from odoo.tools import unique


class StockMove(models.Model):
    _inherit = 'stock.move'

    pack_number = fields.Integer(string="Package Number")
    remarks = fields.Char('Remarks')


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    product_ref = fields.Boolean(string="Product Reference")
    total_package = fields.Integer(compute="_total_packages", string="Packages")

    @api.multi
    def print_pdf_report(self):
        records = self.env['stock.picking'].search([('id', '=', self.id)])

        if records:
            return self.env.ref('packing_list.report_action_packing_list').report_action(records, config=False)

    def _total_packages(self):
        rec = self.env['stock.move.line'].search([('picking_id', '=', self.id)]).mapped('result_package_id')
        test = list(unique(rec))
        self.total_package = len(test)

