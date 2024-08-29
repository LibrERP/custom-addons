# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    mass_mailing_outgoing_pec_server = fields.Boolean(
        string="Use PEC Server",
        config_parameter='mass_mailing.outgoing_pec_server',
        help='Use a specific PEC server.')
    mass_mailing_pec_server_id = fields.Many2one(
        'ir.mail_server', string='PEC Server',
        config_parameter='mass_mailing.pec_server_id',
        domain=[('is_pec', '=', True)]
    )

    @api.onchange('mass_mailing_outgoing_pec_server')
    def _onchange_mass_mailing_outgoing_pec_server(self):
        if not self.mass_mailing_outgoing_pec_server:
            self.mass_mailing_pec_server_id = False
