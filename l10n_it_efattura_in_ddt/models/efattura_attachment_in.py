# © 2019-2022 Marco Tosato - Didotech srl (www.didotech.com)

from odoo import models, fields, api
from odoo.exceptions import UserError


class FatturapaAttachmentIn(models.Model):
    _inherit = "fatturapa.attachment.in"

    ddt_refs = fields.Text(string='Riferimenti DDT', defulat='')

    @api.model
    def create(self, values):
        new_fatturapa_attachment_in = super().create(values)
        new_fatturapa_attachment_in.load_ddt_data()
        return new_fatturapa_attachment_in
    # end create

    @api.multi
    def load_ddt_data(self):

        for fatturapa_att_in in self:

            # Lettura file XML e creazione automatica classi da XML
            wiz_obj = self.env['wizard.import.fatturapa'].with_context(from_attachment=fatturapa_att_in)
            e_invoice = wiz_obj.get_invoice_obj(fatturapa_att_in)

            # Lettura dati relativi ai DDT
            ddt_data = e_invoice.FatturaElettronicaBody[0].DatiGenerali.DatiDDT

            # Lettura numeri DDT e ordinamento
            ddts_list = list({str(ddt_info.NumeroDDT).strip() for ddt_info in ddt_data})
            ddts_list.sort()

            # Fusione numeri DDT in un unica stringa
            ddt_string = '\n'.join(ddts_list)

            # Scritturra stringa DDT
            fatturapa_att_in.ddt_refs = ddt_string
        # end for

    # end load_ddt_data

    @api.multi
    def action_show_related_stock_pickings(self):
        """
            Open stock.picking tree view and show only the pickings
            related to the E-Invoice.
            The stock.picking to be shown must have the ddt_supplier_number
            field matching one of the DDT number reported in the E-Invoice.
        """

        self.ensure_one()

        if self.ddt_refs:
            my_ddts = self.ddt_refs.split('\n')

            action = {
                'name': 'DDT Fattura elettronica',
                'type': 'ir.actions.act_window',
                'res_model': 'stock.picking',
                'view_type': 'list',
                'view_mode': 'list',
                'domain': [
                    ('partner_id', '=', self.xml_supplier_id.id),
                    ('ddt_supplier_number', 'in', my_ddts),
                ],
            }

            return action
        else:
            raise UserError('Nessun DDT collegato alla fattura attuale')
        # end if
    # end action_show_ddt_in_stock_pickings
# end FatturapaAttachmentIn
