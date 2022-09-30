# © 2022 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models, api, _
import logging

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


class ProductCategory(models.Model):
    """
    Add a code field on category
    """
    _inherit = 'product.category'
    code = fields.Char(string="Code", required=False)
