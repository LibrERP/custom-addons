# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    has_lines_without_tax = fields.Boolean(compute='_compute_has_lines_without_tax', store=True)

    def action_confirm(self):
        for order in self:
            if order.state == 'draft':
                if order.has_lines_without_tax:
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'type': 'danger',
                            'title': _("Taxes missing"),
                            'message': order.name + ': ' + _('Please verify that taxes are set on all order lines')
                        }
                    }

        return super().action_confirm()

    @api.depends('order_line.tax_id')
    def _compute_has_lines_without_tax(self):
        for order in self:
            lines_without_taxes = order.order_line.filtered_domain([('display_type', '=', False), ('tax_id', '=', False)])
            order.has_lines_without_tax = bool(lines_without_taxes)
