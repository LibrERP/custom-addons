from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
from odoo.tools import float_compare
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    hide_lines_not_ready = fields.Boolean(
        "Hides lines that have reserved availability equal 0",
        config_parameter='massive_ddt_creation.hide_lines_not_ready')
    massive_ddt_same_term = fields.Boolean(
        "Selected massive DDTs must have same payment term",
        config_parameter='massive_ddt_creation.massive_ddt_same_term')
    allow_more_qty = fields.Boolean(
        "Allows more quantity than reserved availability.",
        config_parameter='massive_ddt_creation.allow_more_qty')
    allow_over_stock = fields.Boolean(
        "Allows more quantity than in stock availability.",
        config_parameter='massive_ddt_creation.allow_over_stock')
