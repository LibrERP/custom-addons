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

from operator import attrgetter

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare

def get_dimension(by_length, by_width, by_height):
    if (by_length.length > by_width.width):
        by_dimension = by_length
        dimension = by_length.length
        if (by_length.length < by_height.height):
            by_dimension = by_height
            dimension = by_height.height
    else:
        by_dimension = by_width
        dimension = by_width.width
        if (by_width.width < by_height.height):
            by_dimension = by_height
            dimension = by_height.height
    return (by_dimension, dimension)


class StockPickingPackagePreparation(models.Model):
    _inherit = 'stock.picking.package.preparation'

    packaging_ids = fields.Many2many('product.packaging',
                                     string="Template Packagings",
                                     domain=[('product_id', '=', False)])

    def get_max_package(self, packaging_ids=None):
        """
            Returns a dictionary containing the largest packaging (in selected ones)
            in terms of length, width, height, dimension (largest at all), volume, weight
        """
        packType = self.env['product.packaging']
        dimension = 0.0
        by_dimension = by_length = by_width = by_height = by_volume = by_weight = packType
        if not packaging_ids:
            packaging_ids = packType.search([('id', '!=', False)])
            # Managed search on all packagings available
        if packaging_ids and (len(packaging_ids) > 1):
            last = len(packaging_ids)-1
            by_length = sorted(packaging_ids, key=attrgetter('length'))[last]
            by_width =  sorted(packaging_ids, key=attrgetter('width'))[last]
            by_height = sorted(packaging_ids, key=attrgetter('height'))[last]
            by_volume = sorted(packaging_ids, key=attrgetter('max_volume'))[last]
            by_weight = sorted(packaging_ids, key=attrgetter('max_weight'))[last]
            by_dimension, dimension = get_dimension(by_length, by_width, by_height)
        return {
                'length': by_length,
                'width': by_width,
                'height': by_height,
                'dimension': dimension,
                'by_dimension': by_dimension,
                'volume':by_volume,
                'weight': by_weight}

    def get_right_package(self, packaging_ids=None, volume=0.0, weight=0.0):
        """
            Returns a packaging adequate to satisfy volume and weight
            to be contained.
        """
        packType = self.env['product.packaging']
        ret = packType
        if packaging_ids:
            by_volume = packType
            by_weight = sorted(packaging_ids, key=attrgetter('max_weight'))
            for packaging_id in by_weight:
                if weight < packaging_id.max_weight:
                    by_weight = packaging_id
                    if volume > 10e-6:
                        if volume < packaging_id.max_volume:
                            by_volume = packaging_id
                        if by_volume == by_weight:
                            ret = packaging_id
                            break
                    else:
                        ret = packaging_id
                        break
        return ret

    def get_max_right_package(self, packaging_ids=None, move_lines=None):
        """
            Returns a packaging adequate to satisfy max move (in weight)
            taken from remaining move lines.
        """
        packType = packList = self.env['product.packaging']
        ret = packType
        if packaging_ids and move_lines:
            for move_line in move_lines:
                packList += self.get_package_by_line(packaging_ids, move_line)
            if packList:
                last = len(packList)-1
                ret = sorted(packList, key=attrgetter('max_weight'))[last]
        return ret

    def get_package_by_line(self, packaging_ids=None, move_line=None):
        """
            Returns a packaging adequate to satisfy volume and weight
            to be contained.
        """
        packType = self.env['product.packaging']
        ret = packType
        if packaging_ids and move_line:
            max_pack = self.get_max_package(packaging_ids)
            move_id = move_line.move_id
            if move_id:
                quantity = move_id.product_uom_qty - move_id.quantity_done
                max_weight = move_line.product_id.weight * quantity
                max_volume = move_line.product_id.volume * quantity
                if max_pack['weight'].max_weight >= max_weight:
                    by_volume = packType
                    by_weight = sorted(packaging_ids, key=attrgetter('max_weight'))
                    for packaging_id in by_weight:
                        if max_weight <= packaging_id.max_weight:
                            by_weight = packaging_id
                            if max_volume > 10e-6:
                                if max_volume <= packaging_id.max_volume:
                                    by_volume = packaging_id
                                if by_volume == by_weight:
                                    ret = packaging_id
                                    break
                            else:
                                ret = packaging_id
                                break
        return ret

    def get_package(self, packaging_ids=None, move_lines=None):
        """
            Returns a packaging adequate to satisfy volume and weight
            to be contained.
        """
        packType = self.env['product.packaging']
        ret = packType
        if packaging_ids:
            max_pack = self.get_max_package(packaging_ids)
            max_product = self.get_max_products(move_lines)
            if max_pack['dimension'] >= max_product['dimension']:
#                 max_load = self.get_max_valuelines(move_lines)  # Get whole weight / volume
                by_volume = packType
                by_weight = sorted(packaging_ids, key=attrgetter('max_weight'))
                for packaging_id in by_weight:
                    if max_product['weight'] < packaging_id.max_weight:
                        by_weight = packaging_id
                        if max_product['volume'] > 10e-6:
                            if max_product['volume'] < packaging_id.max_volume:
                                by_volume = packaging_id
                            if by_volume == by_weight:
                                ret = packaging_id
                                break
                        else:
                            ret = packaging_id
                            break
        return ret

    def get_max_products(self, move_lines=None):
        """
            Returns a dictionary containing the largest products for
            all the requested move.line items, in each dimension or overall, 
            volume and weight.
        """
        productType = self.env['product.product']
        dimension = length = width = height = volume = weight = 0.0
        by_dimension = by_length = by_width = by_height = by_volume = by_weight = productType
        product_ids = productType
        for move_line in move_lines:
            product_ids += move_line.product_id
        if product_ids:
            last = len(product_ids)-1
            by_length = sorted(product_ids, key=attrgetter('length'))[last]
            by_width =  sorted(product_ids, key=attrgetter('width'))[last]
            by_height = sorted(product_ids, key=attrgetter('height'))[last]
            by_volume = sorted(product_ids, key=attrgetter('volume'))[last]
            by_weight = sorted(product_ids, key=attrgetter('weight'))[last]
            length = by_length.length
            width = by_width.width
            height = by_height.height
            volume = by_volume.volume
            weight = by_weight.weight
            by_dimension, dimension = get_dimension(by_length, by_width, by_height)
        return {
            'by_length': by_length,
            'by_width': by_width,
            'by_height': by_height,
            'by_dimension': by_dimension,
            'by_volume':by_volume,
            'by_weight': by_weight,
            'length': length,
            'width': width,
            'height': height,
            'dimension': dimension,
            'volume': volume,
            'weight': weight,
            }

    def get_max_valuelines(self, move_lines=None):
        """
            Returns a dictionary containing the whole volume and weight for
            all the requested pickings.
        """
        volume = 0.0
        weight = 0.0
        for move_line in move_lines:
            qty = move_line.product_qty or 1.0
            volume += qty * move_line.product_id.volume
            weight += qty * move_line.product_id.weight
        return {'volume':volume, 'weight': weight}

    def pack_order_lines_00(self, move_lines, packaging_ids):
        packed_lines = {}
        pre_packing_lines = {}
#         iterations_weigth = iterations_volume = 0
        remaining_lines = self.env['stock.move.line']

        packaging_id = self.get_package(packaging_ids, move_lines)
#         max_packs = self.get_max_package(packaging_ids)
# 
#         packaging_id = max_packs['weight']
        volume_limit = packaging_id.max_volume or 0.0
        weight_limit = packaging_id.max_weight or 0.0
#         max_load = self.get_max_valuelines(move_lines)
# 
#         if (max_load['weight'] <= weight_limit) and (max_load['volume'] <= volume_limit):
#             packaging_id = self.get_right_package(packaging_ids, max_load['volume'], max_load['weight'])
#         else:
#             if (max_load['weight'] > weight_limit):
#                 iterations_weigth = int(max_load['weight'] // weight_limit) + int((max_load['weight'] % weight_limit)>0)
#             if (max_load['volume'] > volume_limit):
#                 iterations_volume = int(max_load['volume'] // volume_limit) + int((max_load['volume'] % volume_limit)>0)
#             iterations = max([iterations_weigth, iterations_volume])
 
        if move_lines:
            iteration = 1
            weight = volume = 0.0
            remaining_lines = move_lines
            for move_line in move_lines:
                if move_line:
                    if not packaging_id:
                        packaging_id = self.get_package(packaging_ids, remaining_lines)
                        volume_limit = packaging_id.max_volume or 0.0
                        weight_limit = packaging_id.max_weight or 0.0
                    qty_line = 0
                    remaining_lines -= move_line
                    this_weight = this_volume = 0.0
                    picking_id = move_line.picking_id
                    location_id = picking_id.location_dest_id
                    values = {
                            'packaging_id': packaging_id.id,
                            'location_id': location_id.id,
                         }

                    quantity = 0.0
                    residual = int(move_line.product_qty - qty_line)
                    reserved = int(move_line.product_uom_qty - qty_line)

                    for item_quant in range(residual):
                        qty_line += 1
                        this_weight = move_line.product_id.weight
                        this_volume = move_line.product_id.volume
                        quantity = 1.0
                        item_name = "{}.{}".format(move_line.id, qty_line)
                        line_value = {
                                    "product_id": move_line.product_id.id,
                                    "quantity": quantity,
                                    "reserved_quantity": quantity if (reserved > 0) else 0,
                                    "location_id": location_id.id,
                                    }
                        if packaging_id:
                            if ((weight+this_weight) < weight_limit) and ((volume+this_volume) < volume_limit):
                                weight += this_weight
                                volume += this_volume
                                pre_packing_lines.update({
                                        item_name: [line_value, move_line],
                                        })
                            else:
                                values.update({
                                    'weight': weight, 'shipping_weight': weight
                                    })
                                item_name = "{}".format(iteration)
                                packed_lines.update({
                                    item_name: [pre_packing_lines, values]
                                    })
                                qty_line = 1
                                weight = volume = 0.0
                                item_name = "{}.{}".format(move_line.id, qty_line)
                                pre_packing_lines = {
                                        item_name: [line_value, move_line],
                                        }
                                weight += this_weight
                                volume += this_volume
    #                             max_load = self.get_max_valuelines(remaining_lines)
    #                             packaging_id = self.get_right_package(packaging_ids, max_load['volume'], max_load['weight'])
                                packaging_id = self.get_package(packaging_ids, remaining_lines)
                                values = {
                                        'packaging_id': packaging_id.id,
                                        'location_id': location_id.id,
                                     }
                                volume_limit = packaging_id.max_volume or 0.0
                                weight_limit = packaging_id.max_weight or 0.0
                                iteration += 1
                        else:
                            weight += this_weight
                            volume += this_volume
                            pre_packing_lines.update({
                                    item_name: [line_value, move_line],
                                    })

                if not packaging_id and pre_packing_lines:
                    values.update({
                             'weight': weight,
                            'shipping_weight': weight,
                        })
                    item_name = "{}".format(iteration)
                    packed_lines.update({
                        item_name: [pre_packing_lines, values]
                        })
                    pre_packing_lines = {}
                    qty_line = 1
                    weight = volume = 0.0
                    iteration += 1

            if pre_packing_lines:
                values.update({'weight': weight, 'shipping_weight': weight})
                item_name = "{}".format(iteration)
                packed_lines.update({
                    item_name: [pre_packing_lines, values]
                    })

        return packed_lines

    def pack_order_lines(self, move_lines, packaging_ids):
        packed_lines = {}
        pre_packing_lines = {}
#         iterations_weigth = iterations_volume = 0
        remaining_lines = self.env['stock.move.line']
        packaging_id = self.env['product.packaging']

        packaging_id = self.get_max_right_package(packaging_ids, move_lines)
 
        if move_lines:
            count_lines = 1
            remaining_lines = move_lines
            weight = volume = 0.0
            for move_line in move_lines:
                if move_line:
                    iteration = 1

                    if not packaging_id:
                        packaging_id = self.get_package_by_line(packaging_ids, move_line)
                    if not packaging_id:
                        packaging_id = self.get_max_right_package(packaging_ids, remaining_lines)

                    volume_limit = packaging_id.max_volume or 0.0
                    weight_limit = packaging_id.max_weight or 0.0
                    qty_line = 0
                    remaining_lines -= move_line
                    this_weight = this_volume = 0.0
                    picking_id = move_line.picking_id
                    location_id = picking_id.location_dest_id
                    values = {
                            'packaging_id': packaging_id.id,
                            'location_id': location_id.id,
                         }

                    quantity = 0.0
                    residual = int(move_line.product_qty - qty_line)
                    reserved = int(move_line.product_uom_qty - qty_line)

                    for item_quant in range(residual):
                        qty_line += 1
                        this_weight = move_line.product_id.weight
                        this_volume = move_line.product_id.volume
                        item_name = "{}.{}".format(move_line.id, iteration)
                        line_value = {
                                    "product_id": move_line.product_id.id,
                                    "quantity": qty_line + quantity,
                                    "reserved_quantity": qty_line + quantity if (reserved > 0) else 0,
                                    "location_id": move_line.location_id.id,
                                    }
                        if packaging_id:
                            check_volume = float_compare(volume_limit, (volume+this_volume), precision_rounding=0.00001) >= 0
                            check_weight = float_compare(weight_limit, (weight+this_weight), precision_rounding=0.00001) >= 0
                            if check_weight and check_volume:
                                weight += this_weight
                                volume += this_volume
                                pre_packing_lines.update({
                                        item_name: [line_value, move_line],
                                        })
                            else:
                                values.update({
                                    'weight': weight, 'shipping_weight': weight
                                    })
                                item_name = "{}".format(count_lines)
                                packed_lines.update({
                                    item_name: [pre_packing_lines, values]
                                    })
                                qty_line = 1
                                iteration += 1
                                count_lines +=1
                                weight = volume = 0.0
                                item_name = "{}.{}".format(move_line.id, iteration)
                                line_value.update({
                                            "quantity": qty_line + quantity,
#                                             "reserved_quantity": qty_line + quantity if (reserved > 0) else 0,
                                            })
                                pre_packing_lines={
                                        item_name: [line_value, move_line],
                                        }

                                weight += this_weight
                                volume += this_volume
    #                             max_load = self.get_max_valuelines(remaining_lines)
    #                             packaging_id = self.get_right_package(packaging_ids, max_load['volume'], max_load['weight'])
                                packaging_id = self.get_max_right_package(packaging_ids, remaining_lines)
                                if not packaging_id:
                                    packaging_id = self.get_package_by_line(packaging_ids, move_line)
                                if packaging_id:
                                    values = {
                                            'packaging_id': packaging_id.id,
                                            'location_id': location_id.id,
                                         }
                                    volume_limit = packaging_id.max_volume or 0.0
                                    weight_limit = packaging_id.max_weight or 0.0
                        else:
                            weight += this_weight
                            volume += this_volume
                            pre_packing_lines.update({
                                    item_name: [line_value, move_line],
                                    })

                    if pre_packing_lines:
                        values.update({
                                 'weight': weight,
                                'shipping_weight': weight,
                            })
                        item_name = "{}".format(count_lines)
                        packed_lines.update({
                            item_name: [pre_packing_lines, values]
                            })

                if not packaging_id and pre_packing_lines:
                    values.update({
                             'weight': weight,
                            'shipping_weight': weight,
                        })
                    item_name = "{}".format(count_lines)
                    packed_lines.update({
                        item_name: [pre_packing_lines, values]
                        })
                    qty_line = 1
                    weight = volume = 0.0
                    iteration += 1
                    count_lines +=1

#             if pre_packing_lines:
#                 values.update({'weight': weight, 'shipping_weight': weight})
#                 item_name = "{}".format(count_lines)
#                 packed_lines.update({
#                     item_name: [pre_packing_lines, values]
#                     })

        return packed_lines

### Overriding standard methods

    @api.multi
    def _generate_pack(self):
        self.ensure_one()
        quant_line_model = self.env['stock.quant']
        pack_model = self.env['stock.quant.package']
        move_line_model = self.env['stock.move.line']
        packaging_model = self.env['product.packaging']
        move_lines = move_line_model.browse()
        for picking in self.picking_ids:
            if picking.state != 'assigned':
                raise UserError(
                    _('All the transfers must be "Ready to Transfer".')
                )
            move_lines |= picking.move_line_ids

        if not move_lines:
            raise UserError(
                _('No transfers to perform.')
            )

        packaging_ids = self.packaging_ids
        if not packaging_ids:
            packaging_ids = packaging_model.search([('product_id', '=', False)])
        # TODO: Manage packagings by the whole set rather dedicated one
        if not packaging_ids:
            raise UserError(
                _('No packagings available.')
            )
        packed_lines = self.pack_order_lines(move_lines, packaging_ids)

        if packed_lines:
            package_ids = pack_model
            weight = shipping_weight = 0.0
            processed_lines = []
            # Packages as dictionary of quants
            for item_package in packed_lines.keys():
                packing_lines = quant_line_model
                pre_packing_lines, values = packed_lines[item_package]
                pack = pack_model.create(values)
                move_lines_to_pack = move_line_model
                for item_in_package in pre_packing_lines.keys():
                    need_update = False
                    this_line, tmp_idx = item_in_package.split('.')
                    idx = int(tmp_idx)
                    line_value, move_line = pre_packing_lines[item_in_package]
                    move_id = move_line.move_id
                    picking_id = move_line.picking_id
                    line_qty = move_line.qty_done
                    item_qty = line_value['quantity']

#                     if (idx < 2):
#                         unreserve_qty = move_id.reserved_availability - move_id.quantity_done
#                         quant_line_model._reset_reserved_quantity(move_line.product_id, move_line.location_id, unreserve_qty, lot_id=move_line.lot_id, package_id=move_line.package_id, owner_id=move_line.owner_id, strict=True)
                    quant_line_model._reset_reserved_quantity(move_line.product_id, move_line.location_id, item_qty, lot_id=move_line.lot_id, package_id=move_line.package_id, owner_id=move_line.owner_id, strict=True)

                    line_value['quantity'] = item_qty
                    quant_line = quant_line_model.create(line_value)
                    if this_line in processed_lines:
                    # introduces new move lines where shipping package is different
                        line_qty = 0
                        move_line = move_line.copy()
                        need_update = True
                    move_lines_to_pack += move_line
                    move_line.with_context(bypass_reservation_update=True).write({
#                     move_line.write({
                            "product_uom_qty": line_qty + item_qty,
                            "qty_done": line_qty + item_qty,
                            "result_package_id": pack.id,
                            })
                    move_id.with_context(skip_update_line_ids=True).write({
#                     move_id.write({
                            "pack_number": int(item_package),
                            "product_weight": move_line.product_id.weight,
                            "product_volume": move_line.product_id.volume,
                            })
#                     move_id.with_context(skip_update_line_ids=True)._compute_reserved_availability()
#                     if need_update:
#                         quant_line._update_reserved_quantity(move_line.product_id, move_line.location_id, (line_qty + item_qty), lot_id=move_line.lot_id, package_id=move_line.package_id, owner_id=move_line.owner_id, strict=True)
                        # Manages reservations for added move lines, where needed adopting different packages.
                    quant_line_model._update_reserved_quantity(move_line.product_id, move_line.location_id, (line_qty + item_qty), lot_id=move_line.lot_id, package_id=move_line.package_id, owner_id=move_line.owner_id, strict=True)
                    packing_lines += quant_line
                    if not(this_line in processed_lines):
                        processed_lines.append(this_line)
#                 package_level = self.env['stock.package_level'].create({
#                         'package_id': pack.id,
#                         'picking_id': picking_id.id,
#                         'location_id': False,
#                         'location_dest_id': values['location_id'],
#                         'move_line_ids': [(6, 0, move_lines_to_pack.ids)]
#                         })

                packed_lines.update({
                    item_package: [packing_lines, values]
                    })

                weight += values['weight']
                shipping_weight += values['shipping_weight']
                packing_lines.write({'package_id': pack.id})
                package_ids += pack
 
            if (len(package_ids) > 1):
                values = {'weight': weight, 'shipping_weight': shipping_weight}
                pack = pack_model.create(values)
                pack.write({'package_ids': [(6, 0, package_ids.ids)]})
 
            self.package_id = pack.id
