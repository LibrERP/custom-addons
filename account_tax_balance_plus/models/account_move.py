# © 2023 Didotech <https://www.didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if 'move_type' in vals and res.move_type != vals['move_type']:
            if not res.duedate_manager_id.invoice_id.id:
                res.move_type = vals['move_type']
        # print(vals)
        return res

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        for move in self:
            if 'move_type' in vals and not self.env.context.get("StopRecursion_movetype_validation"):
                move = move.with_context(StopRecursion_movetype_validation=True)
                if not move.duedate_manager_id.invoice_id.id:
                    move.move_type = vals['move_type']
        # print(vals)
        return res

