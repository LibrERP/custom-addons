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
