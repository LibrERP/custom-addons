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

    @api.multi
    def action_view_invoice(self):
        result = super().action_view_invoice()

        if result['type'] == 'ir.actions.server':
            action_name = 'account.action_invoice_tree1'
            form_view_name = 'account.invoice_form'

            action = self.env.ref(action_name)
            result = action.read()[0]
            if len(self.invoice_ids) > 1:
                result['domain'] = "[('id', 'in', %s)]" % self.invoice_ids.ids
            else:
                form_view = self.env.ref(form_view_name)
                result['views'] = [(form_view.id, 'form')]
                result['res_id'] = self.invoice_ids.id

        return result


class StockPickingPackagePreparation(models.Model):
    _inherit = 'stock.picking.package.preparation'

    @api.multi
    def action_invoice_create(self):
        picking_ids = []
        for package in self:
            package.picking_ids.write({'invoice_state': 'invoiced'})
            picking_ids += package.picking_ids.ids

        invoice_ids = super().action_invoice_create()

        self[0].invoice_id.picking_ids = [(6, False, picking_ids)]

        return invoice_ids
