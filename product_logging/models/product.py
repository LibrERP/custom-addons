# © 2021 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class ProductVariant(models.Model):
    _name = 'product.product'
    _inherit = [
        'product.product',
        'model.logging.mixin',
    ]


class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = [
        'product.template',
        'model.logging.mixin',
    ]
