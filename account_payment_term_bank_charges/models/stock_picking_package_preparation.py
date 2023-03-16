# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import Warning as UserError
import odoo.addons.decimal_precision as dp


class StockPickingPackagePreparation(models.Model):

    _inherit = 'stock.picking.package.preparation'
    _rec_name = 'display_name'
    _order = 'date desc'

    @api.multi
    def other_operations_on_ddt(self, invoice):
        res = super().other_operations_on_ddt(invoice)

        if invoice.invoice_line_ids:
            if invoice.type == 'out_invoice' and invoice.state == 'draft' and invoice.payment_term_id and (
                    invoice.payment_term_id.spese_incasso_id):
                payment_term_model = self.env['account.payment.term']
                spese_incasso = payment_term_model.browse(invoice.payment_term_id.id)
                product_charges_ids = invoice._product_charges_ids()
                for line in invoice.invoice_line_ids:
                    if line.product_id.id in product_charges_ids:
                        invoice.invoice_line_ids -= line
                if spese_incasso:
                    lines = spese_incasso.line_ids.filtered(lambda l: l.payment_method_credit)
                    qty = len(lines)
                    vals = invoice._spese_incasso_vals(spese_incasso.spese_incasso_id, qty)
                    spese = self.env['account.invoice.line'].new(vals)
                    invoice.invoice_line_ids += spese
