# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models


class WizardInventoryReport(models.TransientModel):
    _name = "wizard.inventory.report"
    _description = 'Download inventory data'

    inventory_id = fields.Many2one(comodel_name='stock.inventory')

    data_file = fields.Binary(
        string='Report',
        readonly=True,
    )
    filename = fields.Char()
