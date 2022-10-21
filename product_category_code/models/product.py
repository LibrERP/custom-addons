# © 2022 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    category_code = fields.Char(related='categ_id.code', string='Category Code')
