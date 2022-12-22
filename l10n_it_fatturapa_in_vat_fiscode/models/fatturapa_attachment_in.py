# © 2019-2022 Marco Tosato - Didotech srl (www.didotech.com)

from odoo import models, fields, api


class FatturapaAttachmentIn(models.Model):
    _inherit = 'fatturapa.attachment.in'

    xml_supplier_vat = fields.Char(
        string='Partita IVA (da XML)',
        help='Partita IVA del fornitore come riportata nel documento XML caricato',
        readonly=True,
        indexed=True,
    )

    xml_supplier_fiscal_code = fields.Char(
        string='Codice fiscale (da XML)',
        help='Codice fiscale del fornitore come riportata nel documento XML caricato',
        readonly=True,
        indexed=True,
    )

    def load_extra_data_single(self, e_invoice_obj):
        """Extends load_extra_data_single() method to load data about DDT"""
        super().load_extra_data_single(e_invoice_obj)
        self.load_supplier_vat(e_invoice_obj)
        self.load_supplier_fiscal_code(e_invoice_obj)
    # end load_extra_data_single

    def load_supplier_vat(self, e_invoice_obj):
        self.ensure_one()  # Just in case the method gets called from outside load_extra_data_single method

        vat_obj = e_invoice_obj.FatturaElettronicaHeader.CedentePrestatore.DatiAnagrafici.IdFiscaleIVA

        supplier_vat = str(vat_obj.IdPaese) + str(vat_obj.IdCodice)
        self.xml_supplier_vat = supplier_vat
    # end _load_supplier_vat

    def load_supplier_fiscal_code(self, e_invoice_obj):
        self.ensure_one()  # Just in case the method gets called from outside load_extra_data_single method

        supplier_fiscal_code = str(e_invoice_obj.FatturaElettronicaHeader.CedentePrestatore.DatiAnagrafici.CodiceFiscale)
        self.xml_supplier_fiscal_code = supplier_fiscal_code
    # end _load_supplier_fiscal_code

# end FatturapaAttachmentIn
