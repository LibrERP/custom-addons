# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    task_ids = fields.One2many(
        comodel_name="project.task",
        related="project_id.task_ids",
        string="Project Tasks",
        readonly=True,
    )
