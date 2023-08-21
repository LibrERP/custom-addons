# © 2016 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def _selection_move_type(self):
        return [
            ('other', _('Other')),
            ('liquidity', _('Liquidity')),
            ('receivable', _('Receivable')),
            ('receivable_refund', _('Receivable refund')),
            ('payable', _('Payable')),
            ('payable_refund', _('Payable refund')),
        ]

    move_type_settings = fields.Selection(
        selection='_selection_move_type',
        compute='_compute_move_type_settings', store=True, readonly=True)

    move_type = fields.Selection(
        selection='_selection_move_type',
        string='Entry type',
        # readonly=False,
        # states={'draft': [('readonly', False)]},
        index=True,
        change_default=True,
        default=lambda self: self._context.get('move_type', 'other'),
        required=True,
    )

    @api.multi
    @api.depends(
        'line_ids.account_id.internal_type', 'line_ids.balance',
        'line_ids.account_id.user_type_id.type'
    )
    def _compute_move_type_settings(self):
        def _balance_get(line_ids, internal_type):
            return sum(line_ids.filtered(
                lambda x: x.account_id.internal_type == internal_type).mapped(
                    'balance'))

        for move in self:
            internal_types = move.line_ids.mapped('account_id.internal_type')
            if 'liquidity' in internal_types:
                move.move_type_settings = 'liquidity'
            elif 'payable' in internal_types:
                balance = _balance_get(move.line_ids, 'payable')
                move.move_type_settings = (
                    'payable' if balance < 0 else 'payable_refund')
            elif 'receivable' in internal_types:
                balance = _balance_get(move.line_ids, 'receivable')
                move.move_type_settings = (
                    'receivable' if balance > 0 else 'receivable_refund')
            else:
                move.move_type_settings = 'other'

    def create(self, vals):
        res = super().create(vals)
        # if 'move_type' in vals:
        #     vals['move_type'] = 'other'
        # print(vals)
        return res

    def write(self, vals):
        if self.duedate_manager_id.invoice_id.id and 'move_type' in vals:
            vals['move_type'] = self.move_type_settings
        print(vals)
        return super().write(vals)

