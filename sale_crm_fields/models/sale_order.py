# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    lead_stage_id = fields.Many2one(related="opportunity_id.stage_id", string="Fase Opportunità")
    lead_status = fields.Selection(related="opportunity_id.won_status", string="Stato Opportunità")
