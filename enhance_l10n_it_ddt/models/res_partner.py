# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2020-2021 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2021-04-02
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

from odoo import fields, models

TD_INVOICING_GROUPS = [('nothing', 'One TD - One Invoice'),
                       ('billing_partner', 'Billing Partner'),
                       ('shipping_partner', 'Shipping Partner'),
                       ('code_group', 'Code group')]


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _carriage_condition(self):
        return self.env['res.config.settings']._carriage_condition_get()

    def _goods_description(self):
        return self.env['res.config.settings']._goods_description_get()

    def _transportation_reason(self):
        return self.env['res.config.settings']._transportation_reason_get()

    def _transportation_method(self):
        return self.env['res.config.settings']._transportation_method_get()

    def _ddt_type_method(self):
        return self.env['res.config.settings']._ddt_type_method_get()

    ddt_invoicing_group = fields.Selection(
        TD_INVOICING_GROUPS, 'TD invoicing group',
        default='nothing',
        required=True,
    )

    ### Overridden OCA settings
    carriage_condition_id = fields.Many2one(
        'stock.picking.carriage_condition',
        string='Carriage Condition',
        default=_carriage_condition)
    goods_description_id = fields.Many2one(
        'stock.picking.goods_description',
        string='Goods Description',
        default=_goods_description)
    transportation_reason_id = fields.Many2one(
        'stock.picking.transportation_reason',
        string='Transportation Reason',
        default=_transportation_reason)
    transportation_method_id = fields.Many2one(
        'stock.picking.transportation_method',
        string='Transportation Method',
        default=_transportation_method)
    ### Overridden OCA settings

    ddt_type_id = fields.Many2one(
        'stock.ddt.type',
        string='Preferred Transport Document Type',
        default=_ddt_type_method)

    is_delivery_carrier = fields.Boolean(
        string='Is it a Delivery Carrier',
        help='Choose this option if this partner would be used as delivery carrier.',
        default=False)

