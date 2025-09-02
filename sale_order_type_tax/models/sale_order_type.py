# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class SaleOrderType(models.Model):
    _inherit = "sale.order.type"

    tax_id = fields.Many2one(comodel_name='account.tax', string='Default Tax')
