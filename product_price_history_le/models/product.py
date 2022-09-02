# © 2021-2022 Didotech srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models, fields, api
# import time
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class product_template(models.Model):
    _inherit = 'product.template'

    product_history = fields.One2many(
        'product.price.history',
        'product_tmpl_id',
        string='Price History',
        readonly=True,
        ondelete='cascade'
    )
    price_history_count = fields.Integer(
        "Price History Count", compute='_compute_price_history_count')

    @api.multi
    def _compute_price_history_count(self):
        for t in self:
            t.price_history_count = self.env['product.price.history'].search_count(
                [('product_tmpl_id', '=', t.id)])


    @api.multi
    def write(self, values):
        for prod_template in self:
            if ('lst_price' in values and prod_template.list_price != values['lst_price']) or \
                    ('standard_price' in values and prod_template.standard_price != values['standard_price']):

                history_values = {
                    'user_id': self.env.user.id,
                    'product_id': prod_template.product_variant_id.id,
                    'product_tmpl_id': prod_template.id
                }
                if values.get('list_price', False):
                    history_values.update({
                        'list_price': prod_template.list_price,
                        'new_list_price': values['list_price'],
                    })
                if values.get('standard_price', False):
                    history_values.update({
                        'standard_price': prod_template.standard_price,
                        'new_standard_price': values['standard_price'],

                    })
                self.env['product.price.history'].create(history_values)

        return super(product_template, self).write(values)


class product_product(models.Model):
    _inherit = 'product.product'

    @api.multi
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if not default:
            default = {}
        default.update({
            'product_history': []
        })
        return super(product_product, self).copy(default)
