# © 2023 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields, api


class Project(models.Model):
    _inherit = 'project.project'

    tasks_opened = fields.Integer(compute='compute_opened_tasks', string='Opened')
    tickets_opened = fields.Integer(compute='compute_opened_tickets', string='Opened Tickets')

    @api.depends('tasks')
    def compute_opened_tasks(self):
        for project in self:
            opened_tasks = project.tasks.filtered(lambda t: t.stage_id.name not in ['done', 'Done'])
            project.tasks_opened = len(opened_tasks)

    @api.depends('tasks')
    def compute_opened_tickets(self):
        for project in self:
            opened_tickets = project.ticket_ids.filtered(lambda t: t.stage_id.name not in ['done', 'silent_done', 'Done', 'Silent Done'])
            project.tickets_opened = len(opened_tickets)
