# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, models


class StockDeliveryNoteLine(models.Model):
    _inherit = "stock.delivery.note.line"

    @api.model
    def _prepare_detail_lines(self, moves):
        lines = super()._prepare_detail_lines(moves)

        for line in lines:
            move = self.env['stock.move'].browse(line['move_id'])
            sale_line_name = move.sale_line_id.name
            if sale_line_name:
                line['name'] = sale_line_name
            # if move.move_line_ids:
            #     line['name'] += '\n Matricola/e: n° ' + ', n° '.join(move.move_line_ids.mapped('lot_id').mapped('name'))

        return lines
