# Copyright 2020 Andrei Levin - Didotech srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools.translate import _
import logging
import base64
from odoo.addons.l10n_it_fatturapa.bindings.fatturapa import (
    ContattiType,
    ContattiTrasmittenteType
)
from odoo.exceptions import UserError
from odoo.addons.l10n_it_fatturapa_out.wizard.wizard_export_fatturapa import fatturapaBDS
_logger = logging.getLogger(__name__)


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def saveAttachment(self, fatturapa, number):
        attach_obj = self.env['fatturapa.attachment.out']
        vat = attach_obj.get_file_vat()

        attach_str = fatturapa.toDOM(bds=fatturapaBDS).toprettyxml(
            encoding="UTF-8"
        )
        fatturapaBDS.reset()
        attach_vals = {
            'name': '%s_%s.xml' % (vat, number),
            'datas_fname': '%s_%s.xml' % (vat, number),
            'datas': base64.encodestring(attach_str),
        }
        return attach_obj.create(attach_vals)

    @staticmethod
    def _wep_phone_number(phone):
        """"Remove trailing +39 and all no numeric chars"""
        if phone:
            if phone[0:3] == '+39':
                phone = phone[3:]
            elif phone[0] == '+':
                phone = '00' + phone[1:]
            return ''.join([ch for ch in phone if ch.isdigit()])
        else:
            return ''

    def _setContattiTrasmittente(self, company, fatturapa):
        if not company.phone:
            raise UserError(
                _('Company Telephone number not set.'))
        Telefono = self._wep_phone_number(company.phone)
        if not company.email:
            raise UserError(
                _('Company Email not set.'))
        Email = company.email
        fatturapa.FatturaElettronicaHeader.DatiTrasmissione.\
            ContattiTrasmittente = ContattiTrasmittenteType(
                Telefono=Telefono or None, Email=Email or None)

        return True

    def _setContatti(self, CedentePrestatore, company):
        CedentePrestatore.Contatti = ContattiType(
            Telefono=self._wep_phone_number(company.partner_id.phone) or None,
            Email=company.partner_id.email or None
        )

    def setDettaglioLinea(
        self, line_no, line, body, price_precision, uom_precision
    ):
        """
        Extension checks quantity and unit price
        and updates the values correctly
        Odoo standard balance invoice set quantity as negative
        and unit price as positive in down payment line
        SDI doesn't allow these values
        """

        # patch
        # down payment
        # if quantity is negative (odoo standard invoice balance)
        # and unit price is positive
        if line.quantity < 0 < line.price_unit:
            # set quantity as positive
            line.quantity = line.quantity * -1
            # and set negative the unit price
            line.price_unit = line.price_unit * -1

        return super().setDettaglioLinea(line_no, line, body,
                                         price_precision, uom_precision)
