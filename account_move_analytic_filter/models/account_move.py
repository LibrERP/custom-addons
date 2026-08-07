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
        AnalyticAccount = self.env['account.analytic.account']
        for move in self:
            analytic_ids = set()
            for line in move.invoice_line_ids:
                for key in (line.analytic_distribution or {}):
                    # Keys may hold multi-axis combinations ("id1,id2")
                    for part in str(key).split(','):
                        if part.isdigit():
                            analytic_ids.add(int(part))
            # Drop ids whose analytic account was deleted: the JSON field keeps
            # no foreign key, so dangling ids would break the m2m FK on write.
            existing = AnalyticAccount.browse(analytic_ids).exists()
            move.analytic_account_ids = [Command.set(existing.ids)]
