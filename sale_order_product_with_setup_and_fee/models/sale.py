# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import datetime


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('order_line')
    def onchange_order_line(self):
        order_lines = self.env['sale.order.line']

        if self.order_line:
            if not self.partner_id:
                raise ValidationError('Please set partner and save quotation before adding new products')
            elif not self._origin:
                raise ValidationError('Please save quotation before adding new products')

        # Let's find lines that were already processed
        processed_lines = self.order_line.filtered(
            lambda l: l.id and not l.change == 'product_uom_qty'
                      or not (l.product_id.product_tmpl_id.setup_product_id or l.product_id.product_tmpl_id.fee_product_id)
        )

        # Let's find lines that should be processed
        new_lines = self.order_line.filtered(
            lambda l: not l.id and
                      (l.product_id.product_tmpl_id.setup_product_id or l.product_id.product_tmpl_id.fee_product_id)
                      or l.change == 'product_uom_qty'
        )

        # Let's find connected lines without main line (which was deleted)
        dead_lines = self.order_line.filtered(
            lambda l: l.line_id and l.line_id.id not in processed_lines.ids or l.line_id.change == 'product_uom_qty'
        )

        if dead_lines:
            processed_lines = processed_lines.filtered(
                lambda l: l.id not in dead_lines.ids
            )

        for line in new_lines:
            if not line.id:
                new_prime = line.copy()
            else:
                new_prime = line
                new_prime.change = False

            order_lines += new_prime
            if line.product_id.product_tmpl_id.setup_product_id:
                setup_line = self.get_connected_line(line.product_id.product_tmpl_id.setup_product_id, line, new_prime)
                order_lines += setup_line

            if line.product_id.product_tmpl_id.fee_product_id:
                fee_line = self.get_connected_line(line.product_id.product_tmpl_id.fee_product_id, line, new_prime)
                order_lines += fee_line

        self.order_line = processed_lines + order_lines

        for d_line in dead_lines:
            if d_line.line_id and d_line.line_id.id not in self.order_line.ids:
                dead_lines += d_line.line_id

        dead_lines.write({'state': 'cancel'})

    def write(self, values):
        dead_lines = []
        if 'order_line' in values:
            for line in values['order_line']:
                if line[0] == 2:
                    dead_lines.append(line[1])

        ghost_lines = self.env['sale.order.line']
        for order in self:
            ghost_lines += self.env['sale.order.line'].search([
                ('order_id', '=', order.id),
                # ('id', 'not in', order.order_line.ids)
                ('state', '=', 'cancel')
            ])

        result = super().write(values)

        for d_line in ghost_lines:
            if d_line.id not in dead_lines:
                d_line.unlink()

        return result

    def get_connected_line(self, connected_product, line, new_prime):
        if (len(connected_product.product_variant_ids) > 1
                and len(connected_product.attribute_line_ids) == 1):
            attribute_value = self.env['product.attribute.value'].search([
                ('attribute_id', '=',
                 connected_product.attribute_line_ids[0].attribute_id.id),
                ('qty_min', '<=', line.product_uom_qty),
                ('qty_max', '>=', line.product_uom_qty)
            ])
            if not attribute_value:
                attribute_value = self.env['product.attribute.value'].search([
                    ('attribute_id', '=',
                     connected_product.attribute_line_ids[0].attribute_id.id),
                    ('qty_min', '<=', line.product_uom_qty),
                    ('qty_max', '=', False)
                ])

            product_variants = connected_product.product_variant_ids.filtered(
                lambda r: attribute_value.id in r.attribute_value_ids.ids)
            if product_variants:
                product_variant = product_variants[0]
            else:
                product_variant = False

        else:
            product_variant = connected_product.product_variant_ids[0]

        if product_variant:
            connected_line = self.env['sale.order.line'].create({
                'product_id': product_variant.id,
                'name': connected_product.display_name,
                'product_uom_qty': 1,
                'product_uom': connected_product.uom_id.id,
                'tax_id': connected_product.taxes_id,
                'qty_type': connected_product.qty_type,
                'line_id': new_prime.id,
                'unique_id': line.unique_id
            })
            return connected_line
        else:
            return self.env['sale.order.line']

    def unlink(self):
        return super(SaleOrder, self).unlink()


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    line_id = fields.Many2one(comodel_name='sale.order.line')   #, ondelete='cascade')
    # child_ids = fields.One2many(comodel_name='sale.order.line', inverse_name='line_id')
    unique_id = fields.Float()
    change = fields.Selection([
        ('product_uom_qty', 'Quantity')
    ])

    @api.onchange('product_id')
    def onchange_product_id(self):
        self.unique_id = datetime.datetime.now().timestamp()

    @api.onchange('product_uom_qty')
    def onchange_product_qty(self):
        if self.product_id.product_tmpl_id.setup_product_id or self.product_id.product_tmpl_id.fee_product_id:
            self.change = 'product_uom_qty'
