# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    has_ddt = fields.Boolean(compute='_compute_has_ddt', store=True)
    ddt_number_ids = fields.One2many(comodel_name='stock.delivery.note', compute='_get_ddt_number')

    @api.depends('picking_ids.delivery_note_state')
    def _compute_has_ddt(self):
        for order in self:
            order.has_ddt = order.picking_ids.filtered_domain([('delivery_note_state', '=', 'confirm')])

    @api.depends('picking_ids.delivery_note_id')
    def _get_ddt_number(self):
        for order in self:
            delivery_notes = order.picking_ids.filtered_domain([('delivery_note_state', '=', 'confirm')]).mapped('delivery_note_id')
            order.ddt_number_ids = delivery_notes or False
