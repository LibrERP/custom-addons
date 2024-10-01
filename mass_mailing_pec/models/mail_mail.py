# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models, tools


class MailMail(models.Model):
    _inherit = "mail.mail"

    def _send_prepare_values(self, partner=None):
        res = super(MailMail, self)._send_prepare_values(partner)

        if self.mailing_id.is_pec:
            res['email_to'] = [tools.formataddr((partner.name or "False", partner.l10n_it_pec_email or "False"))]

        return res
