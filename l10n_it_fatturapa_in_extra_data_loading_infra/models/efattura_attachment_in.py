# © 2019-2022 Marco Tosato - Didotech srl (www.didotech.com)

from odoo import models, fields, api


class FatturapaAttachmentIn(models.Model):
    _inherit = 'fatturapa.attachment.in'

    @api.model
    def create(self, values):
        new_fatturapa_attachment_in = super().create(values)
        new_fatturapa_attachment_in.load_extra_data_multi()
        return new_fatturapa_attachment_in
    # end create

    @api.multi
    def load_extra_data_multi(self):

        for fatturapa_att_in in self:

            # Lettura file XML e creazione automatica classi da XML
            wiz_obj = self.env['wizard.import.fatturapa'].with_context(from_attachment=fatturapa_att_in)
            e_invoice_obj = wiz_obj.get_invoice_obj(fatturapa_att_in)

            # Lettura dati relativi ai DDT
            fatturapa_att_in.load_extra_data_single(e_invoice_obj)
        # end for

    # end load_extra_data

    def load_extra_data_single(self, e_invoice_obj):
        self.ensure_one()

        # Load extra data for a single object exploiting the already loaded e_invoice object
        pass
    # end load_extra_data_single

# end FatturapaAttachmentIn
