# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    has_ddt = fields.Boolean(compute='_compute_has_ddt', store=True)

    @api.depends('picking_ids.delivery_note_state')
    def _compute_has_ddt(self):
        for order in self:
            order.has_ddt = order.picking_ids.filtered_domain([('delivery_note_state', '=', 'confirm')])
