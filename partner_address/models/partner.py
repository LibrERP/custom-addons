# © 2023 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    address = fields.Char('Destination', compute="get_partner_address", readonly=True)

    def get_partner_address(self):
        for partner in self:
            partner.address =  ', '.join(filter(None, (partner.name, partner.city, partner.street))) or ''
