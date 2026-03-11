# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class Project(models.Model):
    _inherit = 'project.project'

    def action_view_tasks(self):
        action = super().action_view_tasks()

        ctx = dict(action.get('context', {}))
        ctx['project_kanban'] = True
        action['context'] = ctx

        return action
