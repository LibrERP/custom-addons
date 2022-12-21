# © 2019-2022 Marco Tosato - Didotech srl (www.didotech.com)

from odoo import models, fields, api


class FatturapaAttachmentIn(models.Model):
    _inherit = 'fatturapa.attachment.in'

    xml_invoices_numbers = fields.Char(
        string='Numeri fatture (da XML)',
        help='Numeri delle fatture fornitore contenute nel documento XML caricato',
        readonly=True,
        indexed=True,
    )

    def load_extra_data_single(self, e_invoice_obj):
        """Extends load_extra_data_single() method to load data about DDT"""
        super().load_extra_data_single(e_invoice_obj)
        self.load_invoice_numbers(e_invoice_obj)
    # end load_extra_data_single

    def load_invoice_numbers(self, e_invoice_obj):
        self.ensure_one()  # Just in case the method gets called from outside load_extra_data_single method

        invoices_numbers_list = [
            str(e_invoice.DatiGenerali.DatiGeneraliDocumento.Numero)
            for e_invoice in e_invoice_obj.FatturaElettronicaBody
        ]
        self.xml_invoices_numbers = ','.join(invoices_numbers_list)
    # end _load_invoice_numbers

# end FatturapaAttachmentIn
