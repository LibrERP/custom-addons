# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class StockPickingGoodsAppearance(models.Model):
    _inherit = "stock.picking.goods.appearance"

    code = fields.Char()

    _sql_constraints = [
        ('unique_code', 'UNIQUE(code)', 'code must be unique!')
    ]
