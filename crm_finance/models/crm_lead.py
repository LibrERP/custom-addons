# © 2022 Andrei Levin - Didotech srl
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, exceptions, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    received_payment = fields.Float(
        compute="_compute_received_amount", string="Received Payment"
    )
    remaining_payment = fields.Float(string="Remaining Payment")

    def _tax_on_payment(self, payment, invoice):
        return payment - payment * invoice.amount_tax / invoice.amount_total

    def _compute_received_amount(self):
        for record in self:
            record.received_payment = sum(
                [sum(
                    [sum(
                        [self._tax_on_payment(payment['amount'], invoice) for payment in invoice._get_payments_vals()]
                    ) for invoice in order.invoice_ids]
                ) for order in record.order_ids]
            )
            record.write({'remaining_payment': record.planned_revenue - record.received_payment})
