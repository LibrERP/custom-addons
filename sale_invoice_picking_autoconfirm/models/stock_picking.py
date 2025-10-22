# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class Picking(models.Model):
    _inherit = "stock.picking"

    def lot_numbers_match(self):
        for picking in self:
            if not picking.move_line_ids.lot_numbers_match():
                return False
        return True


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def lot_numbers_match(self):
        for line in self:
            if line.product_id.tracking == 'serial':
                if line.lot_id.id != line.move_id.sale_line_id.lot_id.id:
                    return False

        return True
