# © 2019 - Giovanni Monteverde - Didotech srl
# © 2019 - Trevisan Michele - Didotech srl
# © 2023 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class NewInvoices(models.Model):
    _inherit = 'account.invoice'

    def email_new_invoices(self):
        parameter_model = self.env['ir.config_parameter']

        last_check = parameter_model.get_param('invoice_last_check')
        if not last_check:
            last_check = (datetime.now() - timedelta(days=30)).strftime(DEFAULT_SERVER_DATETIME_FORMAT)

        e_lines = self.env['einvoice.line'].search_read([
            ('create_date', '>', str(last_check))
        ], ('id', 'invoice_id'))

        invoice_ids = [line['invoice_id'][0] for line in e_lines if line['invoice_id']]
        invoice_ids = list(set(invoice_ids))

        if invoice_ids:
            body = u'Nel giorno {} sono state ricevute le seguenti fatture:\n\n'.format(datetime.now().strftime('%d/%m/%Y'))

            # order invoices by date
            invoices = self.env['account.invoice'].search([('id', 'in', invoice_ids)],
                                                              order='date_invoice')
            for invoice in invoices:
                body += f'''<p>Nome fornitore: <strong>{invoice.partner_id.name}</strong></p>
                    <p>Numero fattura: {invoice.reference}</p>
                    <p>Data: {invoice.date_invoice}</p>
                    <p>Importo imponibile: <strong>{invoice.amount_untaxed}</strong></p>
                    <p>Numero registrazione: {invoice.number}</p><br>\n\n'''

                # <p>Importo: <strong>{invoice.amount_total}</strong></p>

            company = self.env.user.company_id
            body += f'{company.name}'
            mail_message = self.env['mail.mail']
            subject = f'{company.name}: Report importazione fatture elettroniche'
            email_from = parameter_model.get_param('email_einvoices_report_from').encode('utf-8')
            email_to = parameter_model.get_param('email_einvoices_report_send_to').encode('utf-8')
            letter = mail_message.create({
                'email_from': email_from,
                'email_to': email_to,
                'subject': subject,
                'body_html': body
            })
            letter.send()

        parameter_model.set_param(
            'invoice_last_check', datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        )
