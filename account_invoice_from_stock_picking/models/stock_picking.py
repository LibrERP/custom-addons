# © 2022-2023 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields, api, _


class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit = [
        _name,
        "stock.invoice.state.mixin",
    ]

    returned_by = fields.Boolean(
        string='Returned by customer',
        default=False
    )

    # On validation Stock Picking became 2binvoiced
    @api.multi
    def action_done(self):
        self.invoice_state = '2binvoiced'
        return super().action_done()
