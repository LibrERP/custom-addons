# © 2021 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = [
        'res.partner',
        'model.logging.mixin',
    ]
