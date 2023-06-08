# © 2023 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    price_vat_included = fields.Float(
        'Price with VAT', compute='_compute_price_with_vat',
        digits=dp.get_precision('Product Price'),
        store=True
    )

    @api.depends('lst_price', 'taxes_id')
    def _compute_price_with_vat(self):
        for product in self:
            if product.taxes_id:
                product.price_vat_included = product.lst_price * (1 + product.taxes_id[0].amount/100)
