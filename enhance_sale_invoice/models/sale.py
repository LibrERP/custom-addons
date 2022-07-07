# -*- encoding: utf-8 -*-
##############################################################################
#
#    Created on : 2022-07-07
#    Author : Fabio Colognesi
#    Copyright: Didotech srl 2020 - 2022
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, models, fields, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('invoice_ids','partner_id')
    def _compute_not_paid_invoice_ids(self):
        for order_id in self:
            partner_id = order_id.partner_id
            if partner_id.parent_id:
                partner_id = partner_id.parent_id
            criteria = [
                ('type', '=', 'out_invoice'),
                ('state', 'not in', ['paid','cancel']),
                '|', 
                ('partner_id', '=', partner_id.id),
                ('partner_id', 'in', partner_id.child_ids.ids),
                ]
            invoice_ids = self.env['account.invoice'].search(criteria)
            order_id.not_paid_invoice_count = len(invoice_ids)

    not_paid_invoice_count = fields.Integer(
        string='Not Paid Invoices',
        compute='_compute_not_paid_invoice_ids')

    @api.multi
    def action_view_to_invoices(self):
        '''
        This function returns an action that display existing invoices for partner
        of given sales order. It can either be a in a list or in a form
        view, if there is only one invoice to show.
        '''
        action = self.env.ref('account.action_invoice_tree').read()[0]

        partner_id = self.partner_id
        if partner_id.parent_id:
            partner_id = partner_id.parent_id
        criteria = [
            ('type', '=', 'out_invoice'),
            ('state', 'not in', ['paid','cancel']),
            '|', 
            ('partner_id', '=', partner_id.id),
            ('partner_id', 'in', partner_id.child_ids.ids),
            ]
        invoice_ids = self.env['account.invoice'].search(criteria)

        if len(invoice_ids) > 1:
            action['domain'] = [('id', 'in', invoice_ids.ids)]
        elif invoice_ids:
            form_view = [(self.env.ref('account.invoice_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoice_ids.id
        return action
