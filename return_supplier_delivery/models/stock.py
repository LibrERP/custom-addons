# Copyright 2023 Didotech  <https://www.didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _


class StockPickingTransportationReason(models.Model):

    _inherit = 'stock.picking.transportation_reason'
    _description = 'Reason for Transportation'

    return_supplier = fields.Boolean(string='Reso fornitore')

