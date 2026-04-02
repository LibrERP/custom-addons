# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, models


class WizardImportFatturapa(models.TransientModel):
    _inherit = "wizard.import.fatturapa"

    @api.model
    def cron_import_fatturapa(self):
        xml_ids = self.env['fatturapa.attachment.in'].search([
            ('e_invoice_parsing_error', '=', False),
            ('registered', '=', False),
            ('is_self_invoice', '=', False)
        ])

        wizard = self.env['wizard.import.fatturapa'].with_context(active_ids=xml_ids.ids).create({
            'e_invoice_detail_level': '2',  # Maximum
            'price_decimal_digits': 3,
            'quantity_decimal_digits': 3,
            'discount_decimal_digits': 2
        })

        invoices_form = wizard.importFatturaPA()
        self.env.cr.commit()
        
        invoices_domain = invoices_form.get('domain', False)
        if invoices_domain:
            invoice_ids = invoices_domain[0][2]
            invoices = self.env['account.invoice'].browse(invoice_ids)
            for invoice in invoices:
                try:
                    invoice.action_invoice_open()
                    self.env.cr.commit()
                except Exception as e:# 1. rollback EVERYTHING done for this invoice
                    self.env.cr.rollback()

                    # 2. clear ORM cache (very important)
                    self.env.clear()

                    # 3. now safely write chatter
                    invoice = self.env['account.invoice'].browse(invoice.id)
                    invoice.message_post(body=_("The invoice has not been validated: '{}'").format(e))

                    # 4. commit ONLY the chatter
                    self.env.cr.commit()

        return True
