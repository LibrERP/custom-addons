# -*- encoding: utf-8 -*-
# © 2021 Andrei Levin - Didotech srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class Cron(models.Model):
    _inherit = 'ir.cron'

    def action_disable_active(self):
        if self.env.context['active_ids']:
            crons = self.browse(self.env.context['active_ids'])
            crons.write({'active': False})
        return True
