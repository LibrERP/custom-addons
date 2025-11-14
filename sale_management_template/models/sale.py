# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models
from datetime import timedelta
from odoo.models import NewId
from .sale_order_newid import SaleOrderNewIdManager
from odoo.exceptions import UserError
from odoo.http import request


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def select_lines(self):
        if self.sale_order_template_id:
            view_id = self.env.ref(
                # 'sale_management_template.view_sale_order_template_line_list'
                'sale_management_template.view_sale_order_template_form'
            ).id

            context = dict(self.env.context)
            if isinstance(self.id, NewId):
                # Should never come here. When we press a button a record is saved
                # Store NewId as a special reference
                context.update({
                    'default_sale_order_ref': SaleOrderNewIdManager.store_order_in_session(request.session, self),
                    'default_template_id': self.sale_order_template_id.id,
                })
            else:
                context.update({
                    'order_id': self.id
                })

            for line in self.sale_order_template_id.sale_order_template_line_ids:
                # if not line.product_id or line.product_id and line.product_id.selected_in_template:
                if line.product_id and line.product_id.selected_in_template:
                    line.check = True

            return {
                'name': _('Select Products'),
                'type': 'ir.actions.act_window',
                'res_model': 'sale.order.template',
                'res_id': self.sale_order_template_id.id,
                'view_mode': 'form',  # should be 'tree,form' without a space
                'view_id': view_id,
                'views': [
                    # [view_id, 'list']
                    [view_id, 'form']
                ],
                'target': 'new',
                'context': context
            }
        else:
            return None

    def add_selected_lines(self):
        template = self.sale_order_template_id.with_context(lang=self.partner_id.lang)

        order_lines = [(5, 0, 0)]
        for line in template.sale_order_template_line_ids.filtered(lambda l: l.check):
            data = self._compute_line_data_for_template_change(line)
            if line.product_id:
                discount = 0
                if self.pricelist_id:
                    price = self.pricelist_id.with_context(uom=line.product_uom_id.id).get_product_price(line.product_id, 1, False)
                    if self.pricelist_id.discount_policy == 'without_discount' and line.price_unit:
                        discount = (line.price_unit - price) / line.price_unit * 100
                        # negative discounts (= surcharge) are included in the display price
                        if discount < 0:
                            discount = 0
                        else:
                            price = line.price_unit

                else:
                    price = line.price_unit

                data.update({
                    'price_unit': price,
                    'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                    'product_uom_qty': line.product_uom_qty,
                    'product_id': line.product_id.id,
                    'product_uom': line.product_uom_id.id,
                    'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                })
                if self.pricelist_id:
                    data.update(self.env['sale.order.line']._get_purchase_price(self.pricelist_id, line.product_id, line.product_uom_id, fields.Date.context_today(self)))
            order_lines.append((0, 0, data))

        self.order_line = order_lines
        self.order_line._compute_tax_id()

        option_lines = []
        for option in template.sale_order_template_option_ids:
            data = self._compute_option_data_for_template_change(option)
            option_lines.append((0, 0, data))
        self.sale_order_option_ids = option_lines

        if template.number_of_days > 0:
            self.validity_date = fields.Date.context_today(self) + timedelta(template.number_of_days)

        self.require_signature = template.require_signature
        self.require_payment = template.require_payment

        if template.note:
            self.note = template.note


class SaleOrderTemplate(models.Model):
    _inherit = "sale.order.template"

    def add_selected_line(self):
        new_lines = self.sale_order_template_line_ids.filtered(lambda l: l.check)
        # order_id = eval(self.env.context.get('order_id'))
        # sale_order = self.env['sale.order'].browse(order_id)

        context = self.env.context
        if context.get('default_sale_order_ref'):
            # Should never pass here. When we press a button a record is saved
            # Handle NewId case
            sale_order = SaleOrderNewIdManager.get_order_from_session(self.env, request.session, context.get('default_sale_order_ref'))
            if not sale_order:
                raise UserError(_("Sale Order not found or session expired"))
        else:
            # Handle regular ID
            order_id = context.get('order_id')
            if order_id:
                sale_order = self.env['sale.order'].browse(order_id)
            else:
                sale_order = self.env['sale.order']

        # sale_order = self.env.context.get('order')
        sale_order.add_selected_lines()
        new_lines.write({'check': False})
        return {'type': 'ir.actions.act_window_close'}


class SaleOrderTemplateLine(models.Model):
    _inherit = "sale.order.template.line"

    check = fields.Boolean()
