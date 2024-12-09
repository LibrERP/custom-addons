# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    setup_product_id = fields.Many2one(comodel_name='product.template')
    fee_product_id = fields.Many2one(comodel_name='product.template')
