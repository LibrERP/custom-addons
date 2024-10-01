# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models
from odoo.osv import expression
from ast import literal_eval


class Mailing(models.Model):
    _inherit = 'mailing.mailing'

    is_pec = fields.Boolean(string="Sent as PEC")

    @api.model
    def default_get(self, fields):
        rec = super(Mailing, self).default_get(fields)
        rec['mail_server_available'] = self.env['ir.config_parameter'].sudo().get_param('mass_mailing.outgoing_mail_server')
        return rec

    def _get_default_mailing_domain(self):
        mailing_domain = super(Mailing, self)._get_default_mailing_domain()

        if self.mailing_type == 'mail' and self.is_pec:
            mailing_domain = expression.AND([[('l10n_it_pec_email', '!=', False)], mailing_domain])

        return mailing_domain

    @api.depends('is_pec')
    def _compute_mailing_domain(self):
        return super()._compute_mailing_domain()

    @api.onchange('is_pec')
    def onchange_is_pec(self):
        if self.mailing_type == 'mail' and self.is_pec:
            self.mail_server_id = self.get_default_pec_server_id()
        elif self.mailing_type == 'mail':
            self.mail_server_id = self._get_default_mail_server_id()

    @api.model
    def get_default_pec_server_id(self):
        server_id = self.env['ir.config_parameter'].sudo().get_param('mass_mailing.pec_server_id')
        try:
            server_id = literal_eval(server_id) if server_id else False
            return self.env['ir.mail_server'].search([('id', '=', server_id)]).id
        except ValueError:
            return False

    def _compute_mail_server_available(self):
        if self.mailing_type == 'mail' and self.is_pec:
            self.mail_server_available = self.env['ir.config_parameter'].sudo().get_param(
                'mass_mailing.outgoing_pec_server')
        else:
            return super(Mailing, self)._compute_mail_server_available()
