# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    tracking = fields.Selection(related='product_tmpl_id.tracking', string='Tracking', readonly=False)
