# © 2021 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, models


class ModelLogging(models.AbstractModel):
    """
    Example usage:

    class ProductVariant(models.Model):
        _name = 'product.product'
        _inherit = [
            'product.product',
            'model.logging.mixin',
        ]
    """

    _name = 'model.logging.mixin'

    @api.multi
    def write(self, values):
        messages = []
        for key in values:
            if values[key] != getattr(self, key):
                messages.append(f'New {key}: {values[key]}')

        if messages:
            self.message_post(body='\n'.join(messages))

        return super().write(values)
