# Copyright 2020 Andrei Levin - Didotech srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class WizardImportFatturapa(models.TransientModel):
    _inherit = "wizard.import.fatturapa"

    def invoiceCreate(
            self, fatt, fatturapa_attachment, FatturaBody, partner_id):

        invoice_id = super().invoiceCreate(fatt, fatturapa_attachment, FatturaBody, partner_id)
        invoice = self.env['account.invoice'].browse(invoice_id)
        if invoice.e_invoice_received_date:
            invoice.date = invoice.e_invoice_received_date
        return invoice.id
