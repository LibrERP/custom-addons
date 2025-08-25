# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        for order in self:
            if order.state == 'draft':
                if order.order_line.filtered_domain([('display_type', '=', False), ('tax_id', '=', False)]):
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'type': 'danger',
                            'title': _("Taxes missing"),
                            'message': _('Please verify that taxes are set on all order lines')
                        }
                    }

        return super().action_confirm()
