#  © 2021 Andrei Levin - Didotech srl
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrder (models.Model):
    _inherit = 'sale.order'

    @api.multi
    def _finalize_invoices(self, invoices, references):
        res = super()._finalize_invoices(invoices, references)
        for invoice in invoices.values():
            for line in invoice.invoice_line_ids:
                if line.related_documents:
                    line.related_documents.write({'lineRef': line.sequence})

        return res
