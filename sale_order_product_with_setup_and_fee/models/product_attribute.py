# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models


class ModelModel(models.Model):
    _inherit = "product.attribute.value"

    qty_min = fields.Integer(readonly=True)
    qty_max = fields.Integer(readonly=True)

    def write(self, values):
        if 'name' in values:
            min_value, max_value = self.min_max(values['name'])
            if min_value:
                values['qty_min'] = min_value
            if max_value:
                values['qty_max'] = max_value

        return super().write(values)

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if 'name' in values:
                min_value, max_value = self.min_max(values['name'])
                if min_value:
                    values['qty_min'] = min_value
                if max_value:
                    values['qty_max'] = max_value

        return super().create(vals_list)

    @staticmethod
    def min_max(name):
        if '-' in name:
            min_value, max_value = name.split('-', 1)
            if min_value.isdigit() and max_value.isdigit():
                pass
            else:
                min_value = False
                max_value = False
        elif '<' in name:
            min_value, max_value = name.split('<', 1)
        elif '>' in name:
            max_value, min_value = name.split('>', 1)
        else:
            min_value = False
            max_value = False

        if min_value:
            min_value = int(min_value)
        if max_value:
            max_value = int(max_value)

        return min_value, max_value
