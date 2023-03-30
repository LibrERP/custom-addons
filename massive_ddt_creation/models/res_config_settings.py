from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
from odoo.tools import float_compare
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    hide_lines_not_ready = fields.Boolean(
        "Hides lines that have no reserved quantity",
        help="Setting to True pickings having no reserved quantity will be hidden. Default False.",
        config_parameter='massive_ddt_creation.hide_lines_not_ready')
    massive_ddt_same_term = fields.Boolean(
        "Selected TDs must have same payment term",
        help="Setting to True pickings will be forced to respect the same payment terms. Default False.",
        config_parameter='massive_ddt_creation.massive_ddt_same_term')
    allow_more_qty = fields.Boolean(
        "Allows more quantity than reserved availability.",
        help="Setting to True pickings will be able to override its reserved quantity availability. Default False.",
        config_parameter='massive_ddt_creation.allow_more_qty')
    allow_over_stock = fields.Boolean(
        "Allows more quantity than in stock availability",
        help="Setting to True pickings will be able to override stock quantity availability. Default False.",
        config_parameter='massive_ddt_creation.allow_over_stock')
    allow_manual_complete_td = fields.Boolean(
        "Allows to complete manually TDs",
        help="Setting to True TD will be left 'in pack' condition, waiting for manual completion, so to be managed manually. Default False.",
        config_parameter='massive_ddt_creation.allow_manual_complete_td')
