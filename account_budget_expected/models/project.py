# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import json
from odoo import fields, models, _


class Project(models.Model):
    _inherit = "project.project"

    def _get_budget_items(self, with_action=True):
        results = super()._get_budget_items(with_action)

        for line_data in results['data']:
            budget_lines = self.env['crossovered.budget.lines'].search(json.loads(line_data['action']['args'])[0])
            line_data['expected'] = budget_lines.expected_amount
        return results
