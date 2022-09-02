# © 2021-2022 Didotech srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class product_price_history(models.Model):
    _inherit = 'product.price.history'
    _description = 'Product Price History'
    _rec_name = 'product_id'
    _order = 'date_to desc'

    # _index_name = 'product_price_history_product_id_index'

    supplier_id = fields.Many2one('res.partner', 'Supplier', readonly=True)
    date_to = fields.Datetime('Date To',default=lambda self: fields.Datetime.now(), readonly=True, required=True)
    product_tmpl_id = fields.Many2one(
        'product.template', 'Product',
        readonly=True,
        ondelete='cascade',
        index=True
    )
    user_id = fields.Many2one('res.users', 'User', readonly=True, required=True, default=lambda self: self.env.user, ondelete='cascade')
    list_price = fields.Float('Previous Sale Price', digits=dp.get_precision('Sale Price'), readonly=True)
    new_list_price = fields.Float('New Sale Price', digits=dp.get_precision('Sale Price'), readonly=True)
    standard_price = fields.Float('Previous Cost Price', digits=dp.get_precision('Account'), readonly=True)
    new_standard_price = fields.Float('New Cost Price', digits=dp.get_precision('Account'), readonly=True)
