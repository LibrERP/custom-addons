from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    def supported_dialects(self):
        return [
            ('amazon', 'Amazon'),
            # ('electrolux', 'Electrolux')
        ]

    xml_dialect = fields.Selection(string="XML Dialect", selection=supported_dialects, required=False)
