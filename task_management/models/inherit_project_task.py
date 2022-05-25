# © 2022 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, api , _


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.multi
    def write(self, vals):
        if len(self) == 1:
            # stage_id changed: update user_id
            if 'stage_id' in vals and not self.user_id:
                vals['user_id'] = self.env.uid
        return super(ProjectTask, self).write(vals)
