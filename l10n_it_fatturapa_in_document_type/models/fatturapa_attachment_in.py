# © 2019-2022 Marco Tosato - Didotech srl (www.didotech.com)

from odoo import models, fields, api


class FatturapaAttachmentIn(models.Model):
    _inherit = 'fatturapa.attachment.in'

    xml_type_td = fields.Char(
        string='Tipo documento (TD)',
        readonly=True,
    )

    xml_type_description = fields.Char(
        string='Tipo Documento',
        readonly=True,
        compute='_compute_xml_type_description',
    )

    def load_extra_data_single(self, e_invoice_obj):
        """Extends load_extra_data_single() method to load data about DDT"""
        super().load_extra_data_single(e_invoice_obj)
        self.load_doc_type_td(e_invoice_obj)
    # end load_extra_data_single

    def load_doc_type_td(self, e_invoice_obj):
        self.ensure_one()  # Just in case the method gets called from outside load_extra_data_single method

        type_td_obj = e_invoice_obj.FatturaElettronicaBody[0].DatiGenerali.DatiGeneraliDocumento.TipoDocumento

        self.xml_type_td = str(type_td_obj)
    # end load_doc_type_td

    def _compute_xml_type_description(self):

        for attachment in self:

            # Search for a description matching the TD code
            descr = self.env['fatturapa.document_type'].search([('code', '=', attachment.xml_type_td)])

            if descr:
                # Description found: show it
                description = descr['name']
            else:
                # No matching description: show an empty string
                description = ''
            # end if

            attachment.xml_type_description = description
        # end for
    # end _compute_xml_type_description
# end FatturapaAttachmentIn
