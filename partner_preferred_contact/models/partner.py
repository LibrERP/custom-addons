# © 2023 Andrei Levin <andrei.levin@didotech.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models, _, Command
# from odoo.exceptions import AccessError, MissingError, ValidationError, UserError
# import logging
# _logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    preferred_contact_id = fields.Many2one('res.partner', 'Partner Contact', help='Preferred contact')
