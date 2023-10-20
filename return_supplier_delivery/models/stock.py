# Copyright 2023 Didotech  <https://www.didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _


class StockPickingTransportationReason(models.Model):

    _inherit = 'stock.picking.transportation_reason'
    _description = 'Reason for Transportation'

    return_supplier = fields.Boolean(string='Reso fornitore')


class StockPickingPackagePreparation(models.Model):

    _inherit = 'stock.picking.package.preparation'

    @api.depends('transportation_reason_id')
    def _compute_is_return(self):
        for record in self:
            record.is_return_supplier = record.transportation_reason_id.return_supplier

    is_return_supplier = fields.Boolean(compute=_compute_is_return, string='Reso')

