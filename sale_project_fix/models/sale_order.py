# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange('project_id')
    def _onchange_project_id(self):
        service_lines = self.order_line.filtered_domain([
            ('product_id.type', '=', 'service')
        ])
        order_projects = service_lines.mapped('project_id')

        # if self.project_id in order_projects:
        #     pass
        if not order_projects:
            service_lines.write({
                'project_id': self.project_id.id
            })
        elif order_projects and self.project_id not in order_projects:
            raise UserError(_("There are other projects already associated with lines of this Sale Order"))
