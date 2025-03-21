# -*- encoding: utf-8 -*-
##############################################################################
#
#    Oddo Addons Module, Open Source   
#    Copyright (C) 2024-2025 Codebeex srl (<http://www.codebeex.com>). All Rights Reserved
#
#    Created on: 2025-03-20
#    Author : odoo
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

from datetime import timedelta

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _expected_date(self):
        self.ensure_one()
        if self.state == 'sale' and self.order_id.date_order:
            order_date = self.order_id.date_order
        else:
            order_date = fields.Datetime.now()
        delay = self.product_id.get_produce_delay()
        delayed = order_date + timedelta(days=(self.customer_lead+delay) or 0.0)
        return delayed
