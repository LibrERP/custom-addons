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

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_ddt_carriage_condition_id = fields.Many2one(
        'stock.picking.carriage_condition',
        string='Carriage Condition',
        config_parameter='res.partner.carriage_condition_id')
    sale_ddt_goods_description_id = fields.Many2one(
        'stock.picking.goods_description',
        string='Goods Description',
        config_parameter='res.partner.goods_description_id')
    sale_ddt_transportation_reason_id = fields.Many2one(
        'stock.picking.transportation_reason',
        string='Transportation Reason',
        config_parameter='res.partner.transportation_reason_id')
    sale_ddt_transportation_method_id = fields.Many2one(
        'stock.picking.transportation_method',
        string='Transportation Method',
        config_parameter='res.partner.transportation_method_id')
    partner_ddt_type_method_id = fields.Many2one(
        'stock.ddt.type',
        string='Transport Document Type',
        help='TD Type to be used as default creating a new contact',
        config_parameter='res.partner.ddt_type_id')

    setup_private_ddt_type_id = fields.Many2one(
        'stock.ddt.type',
        string='TD Type for private customers',
        help='TD Type to be used as default creating a new contact',
        config_parameter='res.partner.private_ddt_type_id')
    setup_business_ddt_type_id = fields.Many2one(
        'stock.ddt.type',
        string='TD Type for business customers',
        config_parameter='res.partner.business_ddt_type_id')
    setup_private_eu_ddt_type_id = fields.Many2one(
        'stock.ddt.type',
        string='TD Type for private EU customers',
        config_parameter='res.partner.private_eu_ddt_type_id')
    setup_business_eu_ddt_type_id = fields.Many2one(
        'stock.ddt.type',
        string='TD Type for business EU customers',
        config_parameter='res.partner.business_eu_ddt_type_id')
    setup_private_extra_eu_ddt_type_id = fields.Many2one(
        'stock.ddt.type',
        string='TD Type for private extra EU customers',
        config_parameter='res.partner.private_extra_eu_ddt_type_id')
    setup_business_extra_eu_ddt_type_id = fields.Many2one(
        'stock.ddt.type',
        string='TD Type for business extra EU customers',
        config_parameter='res.partner.business_extra_eu_ddt_type_id')

    def _carriage_condition_get(self):
        entity_type = self.env['stock.picking.carriage_condition']
        tmp_id = self.env["ir.config_parameter"].sudo().get_param("res.partner.carriage_condition_id") or "0"
        return entity_type.browse(int(tmp_id))

    def _goods_description_get(self):
        entity_type = self.env['stock.picking.goods_description']
        tmp_id = self.env["ir.config_parameter"].sudo().get_param("res.partner.goods_description_id") or "0"
        return entity_type.browse(int(tmp_id))

    def _transportation_reason_get(self):
        entity_type = self.env['stock.picking.transportation_reason']
        tmp_id = self.env["ir.config_parameter"].sudo().get_param("res.partner.transportation_reason_id") or "0"
        return entity_type.browse(int(tmp_id))

    def _transportation_method_get(self):
        entity_type = self.env['stock.picking.transportation_method']
        tmp_id = self.env["ir.config_parameter"].sudo().get_param("res.partner.transportation_method_id") or "0"
        return entity_type.browse(int(tmp_id))

    def _ddt_type_method_get(self):
        entity_type = self.env['stock.ddt.type']
        tmp_id = self.env["ir.config_parameter"].sudo().get_param("res.partner.partner_ddt_type_method_id") or "0"
        return entity_type.browse(int(tmp_id))

    def _get_ddt_type(self, partner_id):
        """
            Returns adequate TD type base on partner data
        """
        country_kind = partner_id.get_country_kind()
        if not (partner_id.company_type == 'company'):
            config_parameter='res.partner.private_ddt_type_id'
            if country_kind > 0:
                config_parameter='res.partner.private_eu_ddt_type_id'
            if country_kind < 0:
                config_parameter='res.partner.private_extra_eu_ddt_type_id'
        else:
            config_parameter='res.partner.business_ddt_type_id'
            if country_kind > 0:
                config_parameter='res.partner.business_eu_ddt_type_id'
            if country_kind < 0:
                config_parameter='res.partner.business_extra_eu_ddt_type_id'

        entity_type = self.env['stock.ddt.type']
        tmp_id = self.env["ir.config_parameter"].sudo().get_param(config_parameter) or "0"
        return entity_type.browse(int(tmp_id))

    def _get_td_conditions(self, partner_id):
        """
            Returns Transport Document conditions, choosing by partner
             or by default values.
        """
        carriage_condition_id = self._carriage_condition_get()
        goods_description_id = self._goods_description_get()
        transportation_reason_id = self._transportation_reason_get()
        transportation_method_id = self._transportation_method_get()

        if partner_id:
            carriage_condition_id = partner_id.carriage_condition_id if partner_id.carriage_condition_id else carriage_condition_id
            goods_description_id = partner_id.goods_description_id if partner_id.goods_description_id else goods_description_id
            transportation_reason_id = partner_id.transportation_reason_id if partner_id.transportation_reason_id else transportation_reason_id
            transportation_method_id = partner_id.transportation_method_id if partner_id.transportation_method_id else transportation_method_id

        return {
                'carriage_condition_id': carriage_condition_id.id,
                'goods_description_id': goods_description_id.id,
                'transportation_reason_id': transportation_reason_id.id,
                'transportation_method_id': transportation_method_id.id,
            }
