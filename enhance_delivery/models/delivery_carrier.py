# -*- encoding: utf-8 -*-
##############################################################################
#
#    LibrERP, Open Source Product Enterprise Management System    
#    Copyright (C) 2020-2021 Didotech srl (<http://didotech.com>). All Rights Reserved
#
#    Created on : 2021-08-12
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

from odoo import api, models, fields


class PriceRanges(models.Model):
    _name = "price.range"
    _description = "Price Ranges"

    carrier_id = fields.Many2one(
        'delivery.carrier',
        string='Delivery Carrier',
        ondelete='cascade',
        required=True)
    min_limit = fields.Float(
        string="Minimum Value on Range [euro]",
        required=True)
    max_limit = fields.Float(
        "Maximum Value on Range [euro]",
        required=True)
    value = fields.Float(
        string="Price Value for Range [euro]",
        default=0.0)
    percent = fields.Integer(
        string="Percentage Value for Range [%]",
        help='Assign value based on percent of evaluated amount.',
        default=0)

    @api.onchange('min_limit')
    def on_change_min_limit(self):
        """
            Adjusts the threshold value.
        """
        if self and self.min_limit:
            if self.min_limit < 0:
                self.min_limit = 0
            if self.min_limit > self.max_limit:
                self.max_limit = self.min_limit

    @api.onchange('max_limit')
    def on_change_max_limit(self):
        """
            Adjusts the threshold value.
        """
        if self and self.max_limit:
            if self.max_limit < 0:
                self.max_limit = 0
            if self.min_limit > self.max_limit:
                self.min_limit = self.max_limit

    @api.onchange('value')
    def on_change_value(self):
        """
            Resets the threshold value.
            Changing fixed value remove percentage.
        """
        if self and self.value:
            self.percent = 0

    @api.onchange('percent')
    def on_change_percent(self):
        """
            Resets the threshold value.
            Changing percentage remove fixed value.
        """
        if self and self.percent:
            self.value = 0.0


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    use_ranges = fields.Boolean(
        string="Use Ranges for Shipping",
        help="Set to True if your shipping cost is based on price ranges. Default value is False.",
        default=False)
    range_line_ids = fields.One2many(
        'price.range', 'carrier_id',
        string='Price Ranges',
        help="Shipping costs based on ranges about Sale Order amount.")

    @api.onchange('use_ranges')
    def on_change_use_ranges(self):
        """
            Resets the margin value, if needed.
        """
        if self and self.use_ranges:
            if self.margin <= 0:
                self.margin = 3

    def get_rated_shipping(self, order_amount):
        """
            Gets rated shipping based on price ranges set for the carrier.
            Anyway it uses fixed price if calculated value is lower than this one.
        """
        ret = self.fixed_price
        max_limit = 0

        for range_line_id in self.range_line_ids:
            max_limit = range_line_id.max_limit
            if(order_amount > range_line_id.min_limit) and (order_amount <= range_line_id.max_limit):
                if range_line_id.value:
                    ret = range_line_id.value
                elif range_line_id.percent:
                    ret = order_amount * (float(range_line_id.percent) / 100.0)
                break

        if (order_amount > max_limit):
            ret = order_amount * (float(self.margin) / 100.0)

        if (ret < self.fixed_price):
            ret = self.fixed_price

        return ret

##########################################################################################3
#        OVERRIDE ORIGNAL METHOD
##########################################################################################3
    def rate_shipment(self, order):
        ''' Compute the price of the order shipment

        :param order: record of sale.order
        :return dict: {'success': boolean,
                       'price': a float,
                       'error_message': a string containing an error message,
                       'warning_message': a string containing a warning message}
                       # TODO maybe the currency code?
        '''
        self.ensure_one()
##########################################################################################
#        INJECT YOUR CODE : SHIPPING PRICE EVALUATION
##########################################################################################
#
        res={}
        if order and self.use_ranges:
            if hasattr(self, 'fixed_rate_shipment'):
                order_amount = order._compute_amount_total_without_delivery()
                res = getattr(self, 'fixed_rate_shipment')(order)
                res['price'] = self.get_rated_shipping(order_amount)
        else:
#
##########################################################################################
#        INJECT YOUR CODE : SHIPPING PRICE EVALUATION
##########################################################################################
            if hasattr(self, '%s_rate_shipment' % self.delivery_type):
                res = getattr(self, '%s_rate_shipment' % self.delivery_type)(order)
                # apply margin on computed price
                res['price'] = float(res['price']) * (1.0 + (float(self.margin) / 100.0))
                # free when order is large enough
                if res['success'] and self.free_over and order._compute_amount_total_without_delivery() >= self.amount:
                    res['warning_message'] = _('Info:\nThe shipping is free because the order amount exceeds %.2f.\n(The actual shipping cost is: %.2f)') % (self.amount, res['price'])
                    res['price'] = 0.0
        return res
##########################################################################################3
#        OVERRIDE ORIGNAL METHOD
##########################################################################################3

