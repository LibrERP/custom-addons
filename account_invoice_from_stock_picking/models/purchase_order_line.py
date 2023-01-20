# © 2023 Didotech srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields, _


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    invoiced = fields.Boolean(
        string="Invoiced",
        copy=False
    )
