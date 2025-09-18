# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    tax_invoice_notes = fields.Text(compute='compute_tax_notes', readonly=True)

    @api.depends('invoice_line_ids.tax_ids', 'invoice_line_ids.tax_ids.tax_note')
    def compute_tax_notes(self):
        for invoice in self:
            invoice.tax_invoice_notes = '\n'.join(self.tax_notes())

    def tax_notes(self):
        self.ensure_one()

        tax_notes = []

        for line in self.invoice_line_ids:
            if line.tax_ids.mapped('tax_note'):
                tax_notes += [tax.tax_note for tax in line.tax_ids if tax.tax_note]

        return tax_notes
