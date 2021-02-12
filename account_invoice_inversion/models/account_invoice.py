# Copyright 2021 Andrei Levin - Didotech srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def invert_invoice_sign(self):
        for invoice in self.browse(self.env.context['active_ids']):
            if invoice.type == 'in_invoice':
                invoice.type = 'in_refund'
                for line in invoice.invoice_line_ids:
                    line.price_unit = line.price_unit * -1
                    line.price_subtotal = line.price_subtotal * -1
                    line.price_total = line.price_total * -1
                    line.price_subtotal_signed = line.price_subtotal_signed * -1

                invoice.compute_taxes()
        return True
