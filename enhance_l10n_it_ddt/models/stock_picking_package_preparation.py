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

    def get_partner_bysaleorder_id(self, kind=''):
        """
            Returns partner invoice address
        """
        ret = None
        sale_ids = list(set([picking_id.sale_id for picking_id in self.picking_ids if picking_id.sale_id]))
        if sale_ids:
            sale_id = sale_ids[0]
            ret = sale_id.partner_id
            if kind == 'address':
                ret = sale_id.partner_shipping_id
            if kind == 'invoice':
                ret = sale_id.partner_invoice_id
        else:
            ret = self.get_partner_reference_id(kind=kind)
        return ret

    def get_partner_reference_id(self, kind='invoice'):
        """
            Returns partner invoice address
        """
        ret = self.partner_id
        addr = self.partner_id.address_get(['delivery', 'invoice'])
        if addr.get(kind, False):
            ret = self.partner_id.browse(addr[kind])
        return ret

    @api.onchange('partner_id', 'ddt_type_id')
    def on_change_partner(self):
        """
            Sets ddt type based on Partner setting or on res.config.settings values.
        """
        if not self.ddt_type_id:
            if self.partner_id.ddt_type_id:
                self.ddt_type_id = self.partner_id.ddt_type_id
            else:
                self.ddt_type_id = self.env['res.config.settings']._get_ddt_type(self.partner_id)
        super(StockPickingPackagePreparation, self).on_change_partner()

    @api.model
    def create(self, vals):
        """
            Computes automatically some fields depending on partner settings.
        """
        res = {}
        ddt_id = super(StockPickingPackagePreparation, self).create(vals)
        partner_invoice_id = ddt_id.get_partner_bysaleorder_id('invoice')
        partner_shipping_id = ddt_id.get_partner_bysaleorder_id('address')
        ddt_type_id = ddt_id.partner_id.ddt_type_id
        if partner_invoice_id:
            if ddt_id.partner_id.ddt_type_id:
                ddt_type_id = ddt_id.partner_id.ddt_type_id
            partner_country_type = partner_invoice_id.get_country_kind_as_char()
            res.update({
                'partner_invoice_id': partner_invoice_id.id,
                'partner_country_type': partner_country_type,
                })
        if partner_shipping_id:
            res.update({
                'partner_shipping_id': partner_shipping_id.id,
                 })
        if ddt_id.partner_id:
            if not ddt_type_id:
                ddt_type_id = self.env['res.config.settings']._get_ddt_type(ddt_id.partner_id)
            if ddt_type_id:
                res.update({
                    'ddt_type_id': ddt_type_id.id,
                    })
            res.update(self.env['res.config.settings']._get_td_conditions(ddt_id.partner_id))
        ddt_id.write(res)
        return ddt_id
    
    
