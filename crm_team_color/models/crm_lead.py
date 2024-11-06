# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    bg_color = fields.Selection(related='team_id.lead_color')
