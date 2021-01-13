# Copyright 2020 Andrei Levin - Didotech srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
# from odoo.tools.translate import _
import logging
from odoo.addons.l10n_it_fatturapa.bindings.fatturapa import (
    DatiDocumentiCorrelatiType,
    CodiceArticoloType
)
_logger = logging.getLogger(__name__)


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    # def saveAttachment(self, fatturapa, number):
    #     curframe = inspect.currentframe()
    #     invoices = inspect.getouterframes(curframe, 2)[1].frame.f_locals['invoices']
    #     partner = invoices[0].partner_id
    #
    #     if partner.xml_dialect:
    #         fatturapa = self.set_custom_tags(fatturapa, invoices[0])
    #
    #     return super().saveAttachment(fatturapa, number)

    # def setDatiOrdineAcquisto(self, inv, body):
    #     if inv.customer_reference:
    #         # 2.1.2.2 <IdDocumento>
    #         body.DatiGenerali.DatiOrdineAcquisto.append(DatiDocumentiCorrelatiType(
    #             IdDocumento=inv.customer_reference
    #         ))
    #
    # def setFatturaElettronicaBody(self, inv, FatturaElettronicaBody):
    #     super().setFatturaElettronicaBody(inv, FatturaElettronicaBody)
    #     self.setDatiOrdineAcquisto(inv, FatturaElettronicaBody)

    def setDettaglioLinea(self, line_no, line, body, price_precision, uom_precision):
        DettaglioLinea = super().setDettaglioLinea(line_no, line, body, price_precision, uom_precision)

        if not line.product_id.barcode:
            customerinfo = self.env['product.customerinfo'].search([
                ('product_id', '=', line.product_id.id),
                ('name', '=', line.invoice_id.partner_id.id)
            ])
            if customerinfo:
                for info in customerinfo:
                    CodiceArticolo = CodiceArticoloType(
                        CodiceTipo=info[0].product_code_type,
                        CodiceValore=info[0].product_code[:35]
                    )
                    DettaglioLinea.CodiceArticolo.append(CodiceArticolo)
            else:
                customerinfo = self.env['product.customerinfo'].search([
                    ('product_tmpl_id', '=', line.product_id.product_tmpl_id.id),
                    ('name', '=', line.invoice_id.partner_id.id)
                ])
                for info in customerinfo:
                    CodiceArticolo = CodiceArticoloType(
                        CodiceTipo=info[0].product_code_type,
                        CodiceValore=info[0].product_code[:35]
                    )
                    DettaglioLinea.CodiceArticolo.append(CodiceArticolo)

        return DettaglioLinea
