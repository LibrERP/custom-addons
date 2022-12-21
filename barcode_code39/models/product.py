# © 2021 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models, tools, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    code39 = fields.Char(
        'Code39', copy=False,
        help="EAN39 Article Number used for product identification.")


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    code39 = fields.Char('Code39', related='product_variant_ids.code39', readonly=False)
