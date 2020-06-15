# -*- coding: utf-8 -*-

from odoo import models, fields


class ConnectorCheckpoint(models.Model):
    _inherit = 'connector.checkpoint'

    message = fields.Text(string="Message", required=False)
