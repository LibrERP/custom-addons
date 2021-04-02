# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2020-2021 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2021-01-09
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


class StockPickingPackagePreparation(models.Model):
    _inherit = 'stock.picking.package.preparation'

    @api.onchange('partner_id', 'ddt_type_id')
    def on_change_partner(self):
        """
            Set Partner invoice address and Country type to help 
             filtering ddt for invoice process
        """
        if self.partner_id.ddt_type_id:
            self.ddt_type_id = self.partner_id.ddt_type_id
        else:
            self.ddt_type_id = self.env['res.config.settings']._get_ddt_type(self.partner_id)
        super(StockPickingPackagePreparation, self).on_change_partner()

