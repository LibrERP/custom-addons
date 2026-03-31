# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    analytic_account_ids = fields.Many2many(
        'account.analytic.account',
        compute='_compute_analytic_accounts',
        store=True
    )

    @api.depends('invoice_line_ids.analytic_distribution')
    def _compute_analytic_accounts(self):
        for move in self:
            analytic_ids = set()
            for line in move.invoice_line_ids:
                if line.analytic_distribution:
                    analytic_ids.update(map(int, line.analytic_distribution.keys()))
            move.analytic_account_ids = [(6, 0, list(analytic_ids))]
