# © 2019-2022 Marco Tosato - Didotech srl (www.didotech.com)

from odoo import models, fields, api
from odoo.exceptions import UserError


class FatturapaAttachmentIn(models.Model):
    _inherit = "fatturapa.attachment.in"

    ddt_refs = fields.Text(string='Riferimenti DDT', defulat='')

    def load_extra_data_single(self, e_invoice_obj):
        """Extends load_extra_data_single() method to load data about DDT"""
        super().load_extra_data_single(e_invoice_obj)
        self.load_ddt_data_single(e_invoice_obj)
    # end load_extra_data_single

    def load_ddt_data_single(self, e_invoice_obj):
        self.ensure_one()  # Just in case the method gets called from outside load_extra_data_single method

        # Lettura dati relativi ai DDT
        ddt_data = e_invoice_obj.FatturaElettronicaBody[0].DatiGenerali.DatiDDT

        # Lettura numeri DDT e ordinamento
        ddts_list = list({str(ddt_info.NumeroDDT).strip() for ddt_info in ddt_data})
        ddts_list.sort()

        # Fusione numeri DDT in un unica stringa
        ddt_string = '\n'.join(ddts_list)

        # Scritturra stringa DDT
        self.ddt_refs = ddt_string
    # end load_ddt_data_single

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
