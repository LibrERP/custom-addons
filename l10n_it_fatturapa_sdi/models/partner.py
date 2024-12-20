# © 2020 Andrei Levin - Didotech srl (www.didotech.com)
# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    invoice_email = fields.Char(
        string="Invoice Email",
        help='If set a copy of Invoice will be sent to this address '
             'after sending to SDI'
    )
