# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models
from odoo.exceptions import UserError


class AccountEdiProxyClientUser(models.Model):
    _inherit = 'account_edi_proxy_client.user'

    proxy_type = fields.Selection(selection_add=[
        ('dummy', 'XML')
    ], ondelete={'dummy': 'cascade'})

    private_key_id = fields.Many2one(required=False)

    # last_download_date = fields.Datetime()

    def _get_proxy_urls(self):
        urls = super()._get_proxy_urls()
        urls['dummy'] = {
            'demo': False,
            'prod': {
                'active': 'http://localhost?wsdl',
                'passive': 'http://localhost?wsdl'
            },
            'test': {
                'active': 'http://localhost?wsdl',
                'passive': 'http://localhost?wsdl'
            },
        }
        return urls

    # def _get_proxy_identification(self, company, proxy_type):
    #     if proxy_type == 'l10n_it_namirial':
    #         if not company.l10n_it_codice_fiscale:
    #             raise UserError(_('Please fill your codice fiscale to be able to receive invoices from FatturaPA'))
    #         return company.partner_id._l10n_it_edi_normalized_codice_fiscale()
    #     return super()._get_proxy_identification(company, proxy_type)
