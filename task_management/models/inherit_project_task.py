# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api , _


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.multi
    def write(self, vals):
        #stage_id changed: update user_id
        if 'stage_id' in vals:
            vals['user_id'] = self.env.uid
            res = super(ProjectTask, self).write(vals)
            return res
