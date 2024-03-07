# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import json
from odoo import fields, models, _

import logging
logger = logging.getLogger(__name__)


class Project(models.Model):
    _inherit = "project.project"

    def _get_budget_items(self, with_action=True):
        results = super()._get_budget_items(with_action)
        total_expected = 0.0
        for line_data in results['data']:
            if isinstance(line_data['action']['args'], list):
                # logger.info(f">>>>>>>>> line_data['action']['args']: {line_data['action']['args']}")
                domain = json.loads(line_data['action']['args'][0])
            else:
                domain = json.loads(line_data['action']['args'])[0]

            budget_lines = self.env['crossovered.budget.lines'].search(domain)
            expected = sum([budget.expected_amount for budget in budget_lines])
            line_data['expected'] = expected
            total_expected += expected

        results['total']['expected'] = total_expected

        return results
