# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class WizardImportFatturapa(models.TransientModel):
    _inherit = "wizard.import.fatturapa"

    def importFatturaPA(self):
        self.ensure_one()

        for fatturapa_attachment in self._get_selected_records():
            fatt = fatturapa_attachment.get_invoice_obj()
            max_precision = self.get_max_precision(fatt)
            if max_precision > self.price_decimal_digits:
                self.price_decimal_digits = max_precision
                self.discount_decimal_digits = max_precision + 2

        return super().importFatturaPA()

    def get_max_precision(self, fatt):
        self.ensure_one()

        max_length = 0

        for fattura in fatt.FatturaElettronicaBody:
            for line in fattura.DatiBeniServizi.DettaglioLinee:
                price = str(line.PrezzoUnitario)
                if "." in price:
                    integer, decimal = price.rsplit(".", 1)
                    if decimal and len(decimal) > max_length:
                        max_length = len(decimal)

        return max_length