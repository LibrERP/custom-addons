# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields


class ProjectProject(models.Model):
    _inherit = "project.project"

    milestone_reached_count = fields.Integer(
        compute="_compute_milestone_counts",
        string="Reached Milestones",
        store=False,
    )
    milestone_total_count = fields.Integer(
        compute="_compute_milestone_counts",
        string="Total Milestones",
        store=False,
    )

    def _compute_milestone_counts(self):
        for project in self:
            total = len(project.milestone_ids)
            reached = sum(1 for m in project.milestone_ids if m.is_reached)
            project.milestone_total_count = total
            project.milestone_reached_count = reached

    def action_view_milestones(self):
        self.ensure_one()
        return {
            "name": "Milestones",
            "type": "ir.actions.act_window",
            "res_model": "project.milestone",
            "view_mode": "list,form",
            "domain": [("project_id", "=", self.id)],
            "context": {"default_project_id": self.id},
        }
