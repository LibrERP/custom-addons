# © 2022 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields, api, _


class StockPickingCarriageCondition(models.Model):
    _inherit = 'stock.picking.package.preparation'

    payment_term_id = fields.Many2one('account.payment.term', compute='_compute_payment_term', string="Termini di Pagamento", store=True)

    @api.multi
    @api.depends('picking_ids', 'picking_ids.sale_id', 'picking_ids.sale_id.payment_term_id')
    def _compute_payment_term(self):
        for ddt in self:
            ddt.payment_term_id = ddt.picking_ids and ddt.picking_ids[0].sale_id and ddt.picking_ids[0].sale_id.payment_term_id.id or False
