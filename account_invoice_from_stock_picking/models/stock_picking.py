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


class StockPickingPackagePreparation(models.Model):
    _inherit = 'stock.picking.package.preparation'

    @api.multi
    def action_invoice_create(self):
        self.picking_ids.write({'invoice_state': 'invoiced'})
        invoice_ids = super().action_invoice_create()
        self.invoice_id.picking_ids = [(6, False, self.picking_ids.ids)]
        return invoice_ids
