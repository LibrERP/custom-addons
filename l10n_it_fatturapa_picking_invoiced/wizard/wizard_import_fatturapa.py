# © 2023 Andrei Levin - Didotech srl (www.didotech.com)

from odoo import models, api, fields


class WizardImportFatturapa(models.TransientModel):
    _inherit = "wizard.import.fatturapa"

    def invoiceCreate(self, fatt, fatturapa_attachment, FatturaBody, partner_id):
        invoice_id = super().invoiceCreate(fatt, fatturapa_attachment, FatturaBody, partner_id)
        invoice = self.env['account.invoice'].browse(invoice_id)

        pickings = invoice.fatturapa_attachment_in_id._get_related_pickings()
        if pickings:
            pickings.write({'invoice_state': 'invoiced'})
            invoice.picking_ids = [(6, False, pickings.ids)]

        return invoice_id
