from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    task_filter = fields.Char("Task Filter")

    def set_values(self):
        """task setting field values"""
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('project_dashboard.task_filter', self.task_filter)
        return res

    def get_values(self):
        """task limit getting field values"""
        res = super(ResConfigSettings, self).get_values()
        value = self.env['ir.config_parameter'].sudo().get_param('project_dashboard.task_filter')
        res.update(
            task_filter=value
        )
        return res
