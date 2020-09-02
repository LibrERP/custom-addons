
from odoo import fields, models


class RepositoryWizard(models.TransientModel):
    _name = 'repository_check.repository_wizard'

    line_ids = fields.Many2many(string="id", comodel_name='repository.check')