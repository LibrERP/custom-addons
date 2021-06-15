# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2020-2021 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2021-05-31
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

from operator import attrgetter

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    product_weight = fields.Float(related='product_id.weight', string="Weight", readonly=True, digits=(6, 2))

    @api.model
    def _reset_reserved_quantity(self, product_id, location_id, quantity, lot_id=None, package_id=None, owner_id=None, strict=False):
        """ Increase the reserved quantity, i.e. increase `reserved_quantity` for the set of quants
        sharing the combination of `product_id, location_id` if `strict` is set to False or sharing
        the *exact same characteristics* otherwise. Typically, this method is called when reserving
        a move or updating a reserved move line. When reserving a chained move, the strict flag
        should be enabled (to reserve exactly what was brought). When the move is MTS,it could take
        anything from the stock, so we disable the flag. When editing a move line, we naturally
        enable the flag, to reflect the reservation according to the edition.

        :return: a list of tuples (quant, quantity_reserved) showing on which quant the reservation
            was done and how much the system was able to reserve on it
        """
        self = self.sudo()
        rounding = product_id.uom_id.rounding
        quants = self._gather(product_id, location_id, lot_id=lot_id, package_id=package_id, owner_id=owner_id, strict=strict)
        reserved_quants = []

        for quant in quants:
            if float_compare(quant.reserved_quantity, quantity, precision_rounding=rounding)>=0:
                quant.write({'reserved_quantity': quant.reserved_quantity - quantity})
            else:
                quant.write({'reserved_quantity': quant.reserved_quantity - quant.reserved_quantity})

            if float_is_zero(quantity, precision_rounding=rounding) or float_is_zero(quant.reserved_quantity, precision_rounding=rounding):
                break
        return reserved_quants


class QuantPackage(models.Model):
    _inherit = "stock.quant.package"

    def get_sorted_lines(self, quant_ids):
        """
            Returns stock.quant lines sorted by weight
        """
        if quant_ids:
            by_weight = sorted(quant_ids, key=attrgetter('product_weight'), reverse=True)
        return by_weight
