# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import logging
import re

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

FATTURAPA_IN_REGEX = '^(IT[a-zA-Z0-9]{11,16}|'\
                     '(?!IT)[A-Z]{2}[a-zA-Z0-9]{2,28})'\
                     '_[a-zA-Z0-9]{1,5}'\
                     '\\.(xml|XML|Xml|zip|ZIP|Zip|p7m|P7M|P7m)'\
                     '(\\.(p7m|P7M|P7m))?$'
RESPONSE_MAIL_REGEX = '(IT[a-zA-Z0-9]{11,16}|'\
                      '(?!IT)[A-Z]{2}[a-zA-Z0-9]{2,28})'\
                      '_[a-zA-Z0-9]{1,5}'\
                      '_MT_[a-zA-Z0-9]{,3}'

fatturapa_regex = re.compile(FATTURAPA_IN_REGEX)
response_regex = re.compile(RESPONSE_MAIL_REGEX)


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.model
    def message_route(self, message, message_dict, model=None, thread_id=None,
                      custom_values=None):
        if any("@pec.fatturapa.it" in x for x in [
            message.get('Reply-To', ''),
            message.get('From', ''),
            message.get('Return-Path', '')]
        ):
            _logger.info("Processing FatturaPA PEC with Message-Id: "
                         "{}".format(message.get('Message-Id')))
            fatturapa_attachments = [x for x in message_dict['attachments']
                                     if fatturapa_regex.match(x.fname)]
            response_attachments = [x for x in message_dict['attachments']
                                    if response_regex.match(x.fname)]
            if response_attachments and fatturapa_attachments:
                return self.manage_pec_fe_attachments(
                    message, message_dict, response_attachments)
            else:
                return self.manage_pec_sdi_notification(message, message_dict)

        elif self._context.get('fetchmail_server_id', False):
            # This is not an email coming from SDI
            fetchmail_server = self.env['fetchmail.server'].browse(
                self._context['fetchmail_server_id'])
            if fetchmail_server.is_fatturapa_pec:
                att = self.find_attachment_by_subject(message_dict['subject'])
                if att:
                    return self.manage_pec_sdi_response(att, message_dict)
                else:
                    fetchmail_server.notify_or_log(_(
                        "PEC message \"%s\" has been read "
                        "but not fetched, as not related to an "
                        "e-invoice.\n"
                        "Please check PEC mailbox %s, at server %s,"
                        " with user %s."
                    ) % (
                        message_dict['subject'],
                        fetchmail_server.name, fetchmail_server.server,
                        fetchmail_server.user
                    ))
                    return []

        return super(MailThread, self).message_route(
            message, message_dict, model=model, thread_id=thread_id,
            custom_values=custom_values)
