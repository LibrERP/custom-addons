# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    direction = fields.Char(size=2, compute='_get_direction')  # , store=True)

    # @api.depends('location_id')
    def _get_direction(self):
        for move in self:
            if move.location_id.usage == move.location_dest_id.usage:
                move.direction = '='
            elif move.location_dest_id.usage == 'customer' or move.location_dest_id.usage == 'supplier':
                move.direction = '-'
            elif move.location_id.usage == 'supplier' or move.location_id.usage == 'customer':
                move.direction = '+'
            elif move.location_id.usage == 'internal' and move.location_dest_id.usage == 'inventory' \
                    or move.location_id.usage == 'inventory' and move.location_dest_id.usage == 'internal':
                move.direction = '<>'
            else:
                move.direction = ''


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    direction = fields.Char(size=2, compute='_get_direction')  # , store=True)

    # @api.depends('location_id')
    def _get_direction(self):
        for move in self:
            if move.location_id.usage == move.location_dest_id.usage:
                move.direction = '='
            elif move.location_dest_id.usage == 'customer' or move.location_dest_id.usage == 'supplier':
                move.direction = '-'
            elif move.location_id.usage == 'supplier' or move.location_id.usage == 'customer':
                move.direction = '+'
            elif move.location_id.usage == 'internal' and move.location_dest_id.usage == 'inventory' \
                    or move.location_id.usage == 'inventory' and move.location_dest_id.usage == 'internal':
                move.direction = '<>'
            else:
                move.direction = ''
