# © 2023 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_shipping_name = fields.Char('Destination', related="partner_shipping_id.address", readonly=True)
