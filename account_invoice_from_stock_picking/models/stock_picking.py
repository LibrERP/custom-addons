#    Copyright (C) 2022 Didotech SRL

from odoo import models, fields, api, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    returned_by = fields.Boolean(
        string='Returned by customer',
        default=False
    )

#  attrs="{'invisible': [('state', '!=', 'done')], 'readonly': [('returned_by', '=', False)]}"
