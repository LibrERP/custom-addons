# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    is_task_progress = fields.Boolean(compute='_compute_task_progress',
                                      string="Task in progress",
                                      store=True)

    @api.multi
    @api.depends('stage_id.name')
    def _compute_task_progress(self):
        task_to_filter = self.env['ir.config_parameter'].sudo().get_param('project_dashboard.task_filter')
        if not task_to_filter:
            task_to_filter = 'In Progress'
        for task in self:
            if isinstance(task.stage_id.name, bool):
                task.is_task_progress = False
                continue
            if task.stage_id.name in task_to_filter:
                task.is_task_progress = True
            else:
                task.is_task_progress = False