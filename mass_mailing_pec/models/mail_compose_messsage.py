# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models, tools


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    # def get_mail_values(self, res_ids):
    #     mail_values_dict = super(MailComposeMessage, self).get_mail_values(res_ids)
    #
    #     if self.mass_mailing_id.is_pec:
    #         # recipients_info = self._process_recipient_values(mail_values_dict)
    #
    #         for res_id, mail_value in mail_values_dict.items():
    #             recipient = self.env[mail_value['model']].browse(res_id)
    #             mail_values_dict[res_id]['email_to'] = recipient.l10n_it_pec_email
    #
    #     return mail_values_dict

    def _process_recipient_values(self, mail_values_dict):
        recipients_info = super(MailComposeMessage, self)._process_recipient_values(mail_values_dict)

        if self.mass_mailing_id.is_pec:
            for res_id, mail_value in mail_values_dict.items():
                recipient = self.env[mail_value['model']].browse(res_id)
                recipients_info[recipient.id] = {
                    'mail_to': [recipient.l10n_it_pec_email],
                    'mail_to_normalized': [
                        tools.email_normalize(recipient.l10n_it_pec_email, strict=False)
                    ]
                }

        return recipients_info
