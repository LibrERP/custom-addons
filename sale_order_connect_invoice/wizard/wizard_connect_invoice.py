# © 2022 Andrei Levin - Didotech srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _


class WizardConnectAccountInvoice(models.TransientModel):
    _name = 'wizard.connect.account.invoice'

    invoice_id = fields.Many2one(comodel_name="account.invoice", string="Invoice", required=True)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Customer", required=True)

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        order = self.env['sale.order'].browse(self.env.context['active_id'])
        res['partner_id'] = order.partner_id.parent_id and order.partner_id.parent_id.id or order.partner_id.id
        return res

    def action_connect_order(self):
        order = self.env['sale.order'].browse(self.env.context['active_id'])
        self.invoice_id.origin = order.name
        return {
            'name': _('Account Invoice'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.invoice',
            'view_mode': 'tree,form',
            'target': 'current',
            'res_id': False,
            'domain': [('id', 'in', order.invoice_ids.ids)]
        }
