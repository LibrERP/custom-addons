# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    parent_id = fields.Many2one(comodel_name='sale.order', string="Parent Order")
    child_ids = fields.One2many(comodel_name='sale.order', inverse_name='parent_id')

    @api.constrains('parent_id')
    def _check_parent_id_recursion(self):
        if self._has_cycle():
            raise ValidationError(_("You cannot create relation to itself"))

    def _get_orders_with_children(self):
        """Return ``self`` expanded with all descendant orders.

        Each order is immediately followed by its own children (depth-first),
        without duplicates, so a parent and one of its children selected
        together are only printed once. Used to include child orders in the
        same PDF when printing from a parent order.
        """
        seen = set()
        ordered_ids = []

        def _collect(order):
            if order.id in seen:
                return
            seen.add(order.id)
            ordered_ids.append(order.id)
            for child in order.child_ids:
                _collect(child)

        for order in self:
            _collect(order)
        return self.browse(ordered_ids)
