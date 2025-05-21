# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class Project(models.Model):
    _inherit = "project.project"

    def write(self, vals):
        result = super(Project, self).write(vals)
        if 'partner_id' in vals:
            for task in self.tasks:
                task.write({'partner_id': self.partner_id and self.partner_id.id or False})
        return result
