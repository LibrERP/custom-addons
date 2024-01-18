# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models

class Rma(models.Model):
    _inherit = "rma"

    supplier_id = fields.Many2one(comodel_name="res.partner", string="Supplier", required=False)
