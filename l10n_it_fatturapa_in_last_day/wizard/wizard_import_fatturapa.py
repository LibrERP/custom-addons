# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, models, fields
from dateutil.relativedelta import relativedelta


class WizardImportFatturapa(models.TransientModel):
    _inherit  = "wizard.import.fatturapa"

    def invoiceCreate(
            self, fatt, fatturapa_attachment, FatturaBody, partner_id
    ):
        invoice_id = super().invoiceCreate(
            fatt=fatt, fatturapa_attachment=fatturapa_attachment, FatturaBody=FatturaBody, partner_id=partner_id
        )

        invoice = self.env['account.invoice'].browse(invoice_id)
        invoice.date = fields.Datetime.now().date().replace(day=1) + relativedelta(months=1) - relativedelta(days=1)

        return invoice_id
