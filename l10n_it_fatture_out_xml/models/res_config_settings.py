# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models
from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    def _set_l10n_it_edi_register_demo_mode(self):
        """
        This function overwrites official function and remove block that permits to return in Demo mode
        """

        for config in self:

            proxy_user = self.env['account_edi_proxy_client.user'].search([
                ('company_id', '=', config.company_id.id),
                ('proxy_type', '=', 'dummy'),
            ], limit=1)

            # real_proxy_users = self.env['account_edi_proxy_client.user'].sudo().search([
            #     ('company_id', '=', config.company_id.id),
            #     ('proxy_type', '=', 'l10n_it_namirial'),
            #     ('id_client', 'not like', 'demo'),
            # ])

            # Update the config as per the selected radio button
            # previous_demo_state = proxy_user.edi_mode
            edi_mode = config.l10n_it_edi_demo_mode

            # If the user is trying to change from a state in which they have a registered official or testing proxy client
            # to another state, we should stop them
            # if real_proxy_users and previous_demo_state != edi_mode:
            #     raise UserError(_("The company has already registered with the service as 'Test' or 'Official', it cannot change."))

            if config.l10n_it_edi_register:
                # There should only be one user at a time, if there are no users, register one
                if not proxy_user:
                    self._create_dummy_user(config.company_id, edi_mode)
                    return

                # If there is a demo user, and we are transitioning from demo to test or production, we should
                # delete all demo users and then create the new user.
                elif proxy_user.id_client[:4] == 'demo' and edi_mode != 'demo':
                    self.env['account_edi_proxy_client.user'].search([
                        ('company_id', '=', config.company_id.id),
                        ('proxy_type', '=', 'dummy'),
                        ('id_client', '=like', 'demo%'),
                    ]).sudo().unlink()
                    self._create_namirial_user(config.company_id, edi_mode)

    def _create_dummy_user(self, company_id, edi_mode):
        self.env['account_edi_proxy_client.user'].create({
            'company_id': company_id.id,
            'proxy_type': 'dummy',
            'edi_identification': 'dummy',
            'id_client': f'dummy-{company_id.id}',
            'edi_mode': edi_mode
        })

    def button_create_proxy_user(self):
        self._create_dummy_user(self.company_id, self.l10n_it_edi_demo_mode)

    @api.depends('company_id.account_edi_proxy_client_ids', 'company_id.account_edi_proxy_client_ids.active')
    def _compute_l10n_it_edi_demo_mode(self):
        for config in self:
            edi_user = self.env['account_edi_proxy_client.user'].search([
                ('company_id', '=', config.company_id.id),
                ('proxy_type', '=', 'dummy'),
            ], limit=1)
            config.l10n_it_edi_demo_mode = edi_user.edi_mode or 'demo'

    @api.depends('company_id.account_edi_proxy_client_ids', 'company_id.account_edi_proxy_client_ids.active')
    def _compute_l10n_it_edi_proxy_current_state(self):
        for config in self:
            proxy_user = config.company_id.account_edi_proxy_client_ids.search([
                ('company_id', '=', config.company_id.id),
                ('proxy_type', '=', 'dummy'),
            ], limit=1)

            config.l10n_it_edi_proxy_current_state = 'inactive' if not proxy_user else 'demo' if proxy_user.id_client[:4] == 'demo' else 'active'

    @api.depends('company_id.account_edi_proxy_client_ids', 'company_id.account_edi_proxy_client_ids.active')
    def _compute_last_download_date(self):
        for config in self:
            proxy_user = config.company_id.account_edi_proxy_client_ids.search([
                ('company_id', '=', config.company_id.id),
                ('proxy_type', '=', 'dummy'),
            ], limit=1)

            config.last_download_date = proxy_user.last_download_date or fields.Datetime.now()

    def _set_last_download_date(self):
        for config in self:
            proxy_user = self.env['account_edi_proxy_client.user'].search([
                ('company_id', '=', config.company_id.id),
                ('proxy_type', '=', 'l10n_it_namirial'),
            ], limit=1)

            proxy_user.last_download_date = self.last_download_date
