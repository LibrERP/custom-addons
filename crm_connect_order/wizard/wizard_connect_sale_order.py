# © 2022 Andrei Levin - Didotech srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _


class WizardConnectSaleOrder(models.TransientModel):
    _name = 'wizard.connect.sale.order'

    sale_order_id = fields.Many2one(comodel_name="sale.order", string="Sale Order", required=True)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Customer", required=True)

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        lead = self.env['crm.lead'].browse(self.env.context['active_id'])
        res['partner_id'] = lead.partner_id.id
        return res

    def action_connect_order(self):
        self.sale_order_id.opportunity_id = self.env.context['active_id']
        order_ids = self.env['sale.order'].search([('opportunity_id', '=', self.env.context['active_id'])])
        return {
            'name': _('Sale Order'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'target': 'current',
            'res_id': False,
            'domain': [('id', 'in', order_ids.ids)]
        }
