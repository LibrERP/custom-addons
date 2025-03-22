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

from odoo import api, fields, models

class ProductProduct(models.Model):
    _inherit = "product.product"

    def get_produce_delay(self):
        """
            Gets produce delay from current active Manufacturing / kit BoM.
        """
        self.ensure_one()
        delay = 0.0
        criteria = [
            ('active', '=', True),
            ('type',  'in', ['normal','kit']),
            '|',
            ('product_tmpl_id', '=', self.product_tmpl_id.id),
            ('product_id', '=', self.id),
        ]
        bom_id = self.env['mrp.bom'].search(criteria, limit=1)
        if bom_id:
            delay = bom_id.produce_delay + bom_id.days_to_prepare_mo
        return delay

    def getRawMaterials(self, level=0, currlevel=0, bomtype=['normal','kit'], add_all=True, unit_qty=1, uom_id=None):
        """
            Returns a flat list of each child, listed once, in a Bom ( level = 0 one level only, level = 1 all levels)
        """
        children = []
        product_ids = self.env['product.product']
        if level == 0 and currlevel > 1:
            return children
        for bomid in self.product_tmpl_id.bom_ids:
            if bomid.type in bomtype:
                req_ratio = 1
                if uom_id:
                    req_ratio = 1 / uom_id.ratio if uom_id.uom_type =='smaller' else uom_id.ratio
                product_uom_id = bomid.product_tmpl_id.uom_id
                bom_qty = bomid.product_qty * unit_qty
                bom_uom = bomid.product_uom_id
                if bom_uom.uom_type =='smaller' and product_uom_id.uom_type =='bigger':
                    bom_ratio = req_ratio * bom_uom.ratio * product_uom_id.ratio
                else:
                    bom_ratio = req_ratio * product_uom_id.ratio / bom_uom.ratio
                for bomline in bomid.bom_line_ids:
                    if not(bomline.product_id in product_ids):
                        product_ids += bomline.product_id
                        product_id = bomline.product_id
                        base_uom_type = product_id.uom_id.uom_type 
                        base_ratio = 1 / product_id.uom_id.ratio if base_uom_type == 'smaller' else product_id.uom_id.ratio
                        uom_type = bomline.product_uom_id.uom_type
                        if uom_type =='smaller':
                            line_ratio = bom_uom.ratio / bomline.product_uom_id.ratio if uom_type =='smaller' else bom_uom.ratio * bomline.product_uom_id.ratio
                        else:
                            line_ratio = bom_uom.ratio * bomline.product_uom_id.ratio if uom_type =='smaller' else bom_uom.ratio / bomline.product_uom_id.ratio
                        base_line_ratio = 1 / bomline.product_uom_id.ratio if uom_type =='smaller' else 1 * bomline.product_uom_id.ratio
                        qty_line = bom_qty * bom_ratio * line_ratio * bomline.product_qty
                        if add_all:
                            children.append((bomline.product_id, qty_line, bomline.product_uom_id))
                        else:
                            if not bomline.product_tmpl_id.bom_ids:
                                children.append((bomline.product_id, qty_line, bomline.product_uom_id))
                        if level == 1:
                            children.extend(bomline.product_id.getRawMaterials(level, currlevel+1, bomtype, add_all, qty_line))
        return children
