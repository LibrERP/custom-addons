# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, models

from odoo.addons.project.models.project_task import CLOSED_STATES


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.depends('stage_id', 'depend_on_ids.state')
    def _compute_state(self):
        for task in self:
            dependent_open_tasks = []
            if task.allow_task_dependencies:
                dependent_open_tasks = [
                    dependent_task
                    for dependent_task in task.depend_on_ids
                    if dependent_task.state not in CLOSED_STATES
                ]
            if dependent_open_tasks:
                if task.state not in CLOSED_STATES:
                    task.state = '04_waiting_normal'
            elif task.state == '04_waiting_normal':
                task.state = '01_in_progress'
