# © 2019-2022 Marco Tosato - Didotech srl (www.didotech.com)

from odoo import models, fields, api
from odoo.exceptions import UserError


class FatturapaAttachmentIn(models.Model):
    _inherit = "fatturapa.attachment.in"

    xml_ddt_refs = fields.Text(
        string='Riferimenti DDT in XML',
        help='Numeri identificativi dei DDT contenuti nell\'XML',
        defulat=''
    )

    xml_ddt_count = fields.Integer(
        string='Num. DDT in XML',
        help='Numero dei DDT rilevati nel documento XML',
        default=0,
    )

    odoo_ddt_count = fields.Integer(
        string='Num. DDT trovati',
        help='Numero dei DDT trovati nel sistema',
        compute='_compute_ddt_stuff',
    )

    ddt_status_display = fields.Char(
        string='DDT trovati',
        help='Numero dei DDT trovati nel sistema rispetto a quelli presenti nel DDT',
        compute='_compute_ddt_stuff',
    )

    ddt_value = fields.Float(
        string='Totale DDT',
        help='Totale valore dei DDT registrati',
        compute='_compute_ddt_stuff',
    )

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
        self.xml_ddt_refs = ddt_string
        self.xml_ddt_count = len(ddts_list)
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

        if self.xml_ddt_refs:

            action = {
                'name': 'DDT Fattura elettronica',
                'type': 'ir.actions.act_window',
                'res_model': 'stock.picking',
                'view_type': 'list',
                'view_mode': 'list',
                'domain': self._get_pickings_domain(),
            }

            return action
        else:
            raise UserError('Nessun DDT collegato alla fattura attuale')
        # end if
    # end action_show_ddt_in_stock_pickings

    @api.multi
    def _compute_ddt_stuff(self):
        for attachment in self:
            # 1 - caricare i DDT
            stock_pickings_list = attachment._get_related_pickings()

            # 2 - chiamare le varie funzioni che usano i DDT per calcolare i campi
            # TODO: COMPLETARE CHIAMANDO I METODI
            attachment._compute_odoo_ddt_count(stock_pickings_list)
            attachment._compute_ddt_status_display()
            attachment._compute_value_from_pickings(stock_pickings_list)
        # end for
    # end _compute_ddt_stuff

    def _compute_odoo_ddt_count(self, stock_pickings_list):
        self.ensure_one()

        # There could be more than one picking for each DDT, so the picking must
        detected_ddts = set([stock_pick['ddt_supplier_number'] for stock_pick in stock_pickings_list])
        self.odoo_ddt_count = len(detected_ddts)

        if self.odoo_ddt_count > self.xml_ddt_count:
            print(
                f'Something strange in fatturapa.attachment.in id '
                f'{self.id}: count of DDT in odoo > count DDT in XML'
            )
        # end if
    # end _compute_odoo_ddt_count

    def _compute_ddt_status_display(self):
        self.ensure_one()
        status = f'{self.odoo_ddt_count} / {self.xml_ddt_count}'
        self.ddt_status_display = status
    # end _compute_ddt_status_display

    def _compute_value_from_pickings(self, stock_pickings_list):
        self.ensure_one()

        total_value: int = 0

        # TODO: completare calcolando valore merci da DDT
        # 1 - Recuperare tutti gli stock pickings relativi a questo attachment
        #     Già fatto, viene passato come parametro

        # 2 - Per ogni stock.picking recuperare il valore
    # end _compute_value_from_pickings

    def _get_pickings_domain(self):
        self.ensure_one()

        my_ddts = self.xml_ddt_refs.split('\n')

        pickings_domain = [
            ('partner_id', '=', self.xml_supplier_id.id),
            ('ddt_supplier_number', 'in', my_ddts),
            ('state', '=', 'done'),
        ]

        return pickings_domain
    # end _get_pickings_domain

    def _get_related_pickings(self):
        self.ensure_one()

        domain = self._get_pickings_domain()
        ddt_list = self.env['stock.picking'].search(domain)

        return ddt_list
    # end _get_my_ddt
# end FatturapaAttachmentIn
