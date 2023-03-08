#    Copyright (C) 2023 Didotech srl (<https://www.didotech.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Sale(models.Model):
    _inherit = "sale.order"

    def create(self, vals):
        order = super().create(vals)
        if order.order_line:
            order.update_sequence()
        return order

    def update_sequence(self):
        if self.order_line:
            sequences = set(self.order_line.mapped('sequence'))
            if len(sequences) == 1:
                counter = 0
                for line in self.order_line:
                    seq = line.sequence
                    line.write({
                        'sequence': seq + counter
                    })
                    counter += 1

    @api.multi
    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            order.update_sequence()

        return res
