# © 2023 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime

import logging
# import pytz

from odoo import api, fields, models
# from odoo.osv import expression

_logger = logging.getLogger(__name__)


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=False, )

    @api.model
    def create(self, values):
        activity = super().create(values)

        if activity.res_model == 'res.partner':
            activity.partner_id = activity.res_id
        else:
            object = self.env[activity.res_model].browse(activity.res_id)
            if hasattr(object, 'partner_id'):
                activity.partner_id = object.partner_id.id

        return activity

    # def write(self, values):
    #     activity = super().write(values)
    #
    #     return activity
