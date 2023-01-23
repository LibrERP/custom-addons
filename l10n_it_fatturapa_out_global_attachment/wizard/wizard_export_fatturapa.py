# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2023 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2023-01-17
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import base64
from odoo import api, models, fields
from odoo.exceptions import UserError
from odoo.addons.l10n_it_fatturapa.bindings.fatturapa import (
    AllegatiType,
)


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"
    _description = "Export E-invoice"

    def _attachment_list(self):
        context = self.env.context
        active_id = context.get('active_id', False)
        active_model = context.get('active_model', False)
        if not (active_id and active_model):
            raise UserError('Missing active_id or active_model')

        model = self.env[active_model].browse(active_id)

        description = []
        if model.company_id:
            for attachement in model.company_id.fatturapa_doc_attachments:
                description.append("* {name}".format(name=attachement.datas_fname))

        if description:
            attachment_list = "<strong>ATTENZIONE CONTIENE I SEGUENTI ALLEGATI GLOBALI:</strong> <br>" + '<br>'.join(
                description)
        else:
            attachment_list = ''
        return attachment_list

    def _get_attachement_list(self):
        attachment_list = self._attachment_list()
        for att in self:
            att.attachment_list = attachment_list

    attachment_list = fields.Text(compute='_get_attachement_list', string="Allegati")

    @api.model
    def default_get(self, fields):
        res = super(WizardExportFatturapa, self).default_get(fields)
        res['attachment_list'] = self._attachment_list()
        return res

    def setAttachments(self, invoice, body):
        super(WizardExportFatturapa, self).setAttachments(invoice, body)
        if invoice.company_id.fatturapa_doc_attachments:
            for doc_id in invoice.company_id.fatturapa_doc_attachments:
                # Field Attachment is of Base64 type, so data is encoded automatically when put inside
                # Our attachments are already Base64 encoded, so we should decode them
                AttachDoc = AllegatiType(
                    NomeAttachment=doc_id.datas_fname,
                    Attachment=base64.b64decode(doc_id.datas)
                )
                body.Allegati.append(AttachDoc)

        return True
