# © 2018-2022 Andrei Levin - Didotech srl (www.didotech.com)
# © 2024-2025 Andrei Levin - Codebeex srl (www.codebeex.com)

import datetime
from odoo import models, fields
from odoo.tools import (DEFAULT_SERVER_DATETIME_FORMAT,
                        DEFAULT_SERVER_DATE_FORMAT)
from odoo.tools.translate import _
from odoo.exceptions import UserError
import logging

logger = logging.getLogger(__name__)


class WizardImportInvoice(models.TransientModel):
    _name = "wizard.import.passive.invoice"
    _description = 'Wizard Import Passive Invoice from SDI'

    def get_last_download_date(self):
        # last_xmls = self.env['fatturapa.attachment.in'].search(
        #     [('e_invoice_received_date', '!=', False)],
        #     order='e_invoice_received_date desc', limit=1)
        last_xmls = self.env['fatturapa.attachment.in'].search(
            [('sdi_download_date', '!=', False)],
            order='sdi_download_date desc', limit=1)

        if last_xmls:
            return last_xmls[0].e_invoice_received_date.date()
        else:
            return datetime.date.today()

    def get_default(self):
        company = self.env['res.users'].browse(self.env.uid).company_id
        config = company.sdi_channel_id

        if config.passive_invoice_host:
            # try to set as default last date
            last_xml_date_date = self.get_last_download_date().strftime(
                DEFAULT_SERVER_DATETIME_FORMAT)
        else:
            raise UserError(_('Please set destination host (passive_invoice_host) for passive invoice'))

        return last_xml_date_date

    def _get_dummy_name(self):
        self.name = '...'

    name = fields.Char(compute=_get_dummy_name, string='Name')
    start_import_date = fields.Date(
        'Data inizio importazione', required=True, default=get_default)

    def import_sdi_invoice(self):
        raise UserError(_(
            'Please install module specific for your SdI provider'))
