# © 2021 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = [
        'sale.order',
        'model.logging.mixin',
    ]
