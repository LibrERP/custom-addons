# © 2023 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields


class StockPickingPackagePreparation(models.Model):
    _inherit = 'stock.picking.package.preparation'

    partner_shipping_name = fields.Char('Address', related="partner_shipping_id.address", readonly=True)
