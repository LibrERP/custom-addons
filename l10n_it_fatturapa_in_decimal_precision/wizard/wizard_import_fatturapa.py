# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models


class WizardImportFatturapa(models.TransientModel):
    _inherit = "wizard.import.fatturapa"

    @api.multi
    def importFatturaPA(self):
        self.ensure_one()

        for fatturapa_attachment in self.env['fatturapa.attachment.in'].browse(self.env.context.get('active_ids', False)):
            fatt = fatturapa_attachment.get_invoice_obj()
            max_precision = self.get_max_precision(fatt)
            if max_precision > self['price_decimal_digits']:
                self['price_decimal_digits'] = max_precision

        return super().importFatturaPA()

    @api.multi
    def get_max_precision(self, fatt):
        self.ensure_one()

        max_length = 0

        for fattura in fatt.FatturaElettronicaBody:
            for line in fattura.DatiBeniServizi.DettaglioLinee:
                price = str(line.PrezzoUnitario)
                if '.' in price:
                    integer, decimal = str(line.PrezzoUnitario).rsplit('.', 1)
                    if decimal and len(decimal) > max_length:
                        max_length = len(decimal)

        return max_length

    def _prepareInvoiceLine(self, credit_account_id, line, wt_founds=False):
        retLine = super()._prepareInvoiceLine(
            credit_account_id, line, wt_founds=wt_founds)
        retLine['fatturapa_xml_imported'] = True
        retLine['fatturapa_xml_price_unit'] = float(line.PrezzoUnitario)
        retLine['fatturapa_xml_quantity'] = (
            1.0 if line.Quantita is None else float(line.Quantita)
        )
        retLine['fatturapa_xml_discount'] = retLine.get('discount', 0.0)
        return retLine

    def _prepareInvoiceLineAliquota(self, credit_account_id, line, nline):
        retLine = super()._prepareInvoiceLineAliquota(
            credit_account_id, line, nline)
        retLine['fatturapa_xml_imported'] = True
        retLine['fatturapa_xml_price_unit'] = float(line.ImponibileImporto)
        retLine['fatturapa_xml_quantity'] = 1.0
        retLine['fatturapa_xml_discount'] = 0.0
        return retLine

    def _addGlobalDiscount(self, invoice_id, DatiGeneraliDocumento):
        invoice = self.env['account.invoice'].browse(invoice_id)
        existing_ids = set(invoice.invoice_line_ids.ids)
        result = super()._addGlobalDiscount(
            invoice_id, DatiGeneraliDocumento)
        new_lines = invoice.invoice_line_ids.filtered(
            lambda l: l.id not in existing_ids)
        for ln in new_lines:
            ln.write({
                'fatturapa_xml_imported': True,
                'fatturapa_xml_price_unit': ln.price_unit,
                'fatturapa_xml_quantity': ln.quantity,
                'fatturapa_xml_discount': ln.discount or 0.0,
            })
        return result