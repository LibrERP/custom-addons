# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).


from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    number_of_processes = fields.Integer(
        related='company_id.number_of_processes',
        readonly=False,
    )
