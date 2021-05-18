# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2020-2021 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2021-02-18
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
import odoo.addons.decimal_precision as dp


class ProductPackaging(models.Model):
    _inherit = 'product.packaging'

    def _one_computed_category_length(self):
        return self._one_get_category_uom_id(category='length')

    def _computed_category_height(self):
        if self.height_uom:
            self.height_uom_cat = self.height_uom.category_id.id
        else:
            self.height_uom_cat = self._one_get_category_uom_id(category='length')

    def _computed_category_width(self):
        if self.width_uom:
            self.width_uom_cat = self.width_uom.category_id.id
        else:
            self.width_uom_cat = self._one_get_category_uom_id(category='length')

    def _computed_category_length(self):
        if self.length_uom:
            self.length_uom_cat = self.length_uom.category_id.id
        else:
            self.length_uom_cat = self._one_get_category_uom_id(category='length')

    def _computed_category_volume(self):
        if self.volume_uom:
            self.volume_uom_cat = self.volume_uom.category_id.id
        else:
            self.volume_uom_cat = self._one_get_category_uom_id(category='volume')

    def _one_computed_category_volume(self):
        return self._one_get_category_uom_id(category='volume')

    def _computed_category_weight(self):
        if self.weight_uom:
            self.weight_uom_cat = self.weight_uom.category_id.id
        else:
            self.weight_uom_cat = self._one_get_category_uom_id(category='weight')

    def _one_computed_category_weight(self):
        return self._one_get_category_uom_id(category='weight')

    def _get_length_uom_id(self):
        return self._get_default_uom_id()

    def _get_volume_uom_id(self):
        return self._get_default_uom_id(category="volume")

    def _get_weight_uom_id(self):
        return self._get_default_uom_id(category="weight")

    def _get_category_uom_id(self, category="length"):
        criteria = [('measure_type', '=', category)]
        return self.env["uom.category"].search(criteria, limit=1, order='id')

    @api.model
    def _one_get_category_uom_id(self, category="length"):
        criteria = [('measure_type', '=', category)]
        return self.env["uom.category"].search(criteria, limit=1, order='id')

    height_uom = fields.Many2one(
        'uom.uom', 'Unit of Measure',
        default=_get_length_uom_id, required=True,
        help="Default unit of measure used for all stock operations.")
    height_uom_cat = fields.Integer(
        default=_one_computed_category_length,
        compute="_computed_category_height")
    width_uom = fields.Many2one(
        'uom.uom', 'Unit of Measure',
        default=_get_length_uom_id, required=True,
        help="Default unit of measure used for all stock operations.")
    width_uom_cat = fields.Integer(
        default=_one_computed_category_length,
        compute="_computed_category_width")
    length_uom = fields.Many2one(
        'uom.uom', 'Unit of Measure',
        default=_get_length_uom_id, required=True,
        help="Default unit of measure used for all stock operations.")
    length_uom_cat = fields.Integer(
        default=_one_computed_category_length,
        compute="_computed_category_length")
    volume_uom = fields.Many2one(
        'uom.uom', 'Unit of Measure',
        default=_get_volume_uom_id, required=True,
        help="Default unit of measure used for all stock operations.")
    volume_uom_cat = fields.Integer(
        default=_one_computed_category_volume,
        compute="_computed_category_volume")
    weight_uom = fields.Many2one(
        'uom.uom', 'Unit of Measure',
        default=_get_weight_uom_id, required=True,
        help="Default unit of measure used for all stock operations.")
    weight_uom_cat = fields.Integer(
        default=_one_computed_category_weight,
        compute="_computed_category_weight")
    max_volume = fields.Float('Max Volume',
        digits=dp.get_precision('Volume'),
        compute="_compute_package_volume",
        help='Maximum volume shippable in this packaging')

    def _get_default_uom_id(self, category="length"):
        ret = False
        category_id = self._get_category_uom_id(category=category)
        if category_id:
            criteria = [('uom_type', '=', 'reference'),
                        ('category_id', '=', category_id.id),
                    ]
            ret = self.env["uom.uom"].search(criteria, limit=1, order='id').id
        return ret

    def _get_package_volume(self):
        """
            Returns package volume allowable for this package.
        """
        ret = 0
        if self.length and self.width and self.height:
            ratio = self.length_uom.get_ratio * self.width_uom.get_ratio * self.height_uom.get_ratio
            ret = ratio * self.volume_uom.get_ratio * self.length * self.width * self.height
        return ret

    @api.onchange('length', 'width', 'height','volume_uom','length_uom','width_uom','height_uom')
    def _compute_package_volume(self):
        """
            Sets maximum package volume allowable for this package.
        """
        for package in self:
            package.max_volume = package._get_package_volume()
            package.write({'max_volume': package.max_volume})


 