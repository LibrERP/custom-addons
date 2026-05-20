# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.model_create_multi
    def create(self, vals_list):
        tasks = super().create(vals_list)
        tasks._sync_milestone_deadline(self.env["project.milestone"])
        return tasks

    def write(self, vals):
        track = "milestone_id" in vals or "date_deadline" in vals
        previous = {t.id: t.milestone_id for t in self} if track else {}
        res = super().write(vals)
        if track:
            old_milestones = self.env["project.milestone"].browse(
                {m.id for m in previous.values() if m}
            )
            self._sync_milestone_deadline(old_milestones)
        return res

    @api.onchange("milestone_id", "date_deadline")
    def _onchange_sync_milestone_deadline(self):
        for task in self:
            milestones = task.milestone_id | task._origin.milestone_id
            for milestone in milestones:
                milestone._recompute_deadline_from_tasks(exclude_task=task)

    def _sync_milestone_deadline(self, extra_milestones):
        milestones = (self.mapped("milestone_id") | extra_milestones).exists()
        for milestone in milestones:
            milestone._recompute_deadline_from_tasks()


class ProjectMilestone(models.Model):
    _inherit = "project.milestone"

    def _recompute_deadline_from_tasks(self, exclude_task=None):
        self.ensure_one()
        tasks = self.task_ids
        if exclude_task is not None:
            # In onchange context the in-memory task is not yet persisted to
            # milestone.task_ids; merge it in (or out) so we use the edited state.
            tasks = (tasks - exclude_task._origin) | (
                exclude_task if exclude_task.milestone_id == self else self.env["project.task"]
            )
        dates = [t.date_deadline for t in tasks if t.date_deadline]
        if not dates:
            return
        new_deadline = max(dates).date()
        if self.deadline != new_deadline:
            self.deadline = new_deadline
