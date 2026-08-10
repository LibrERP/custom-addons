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
