# © 2022 - Didotech srl <https://www.didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from odoo import api, models, _

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    @api.model
    def send_email(self, message, mail_server_id=None, smtp_server=None, smtp_port=None,
                   smtp_user=None, smtp_password=None, smtp_encryption=None, smtp_debug=False,
                   smtp_session=None):
        company = self.env.user.company_id
        if company.email_node == company.local_node:
            return super().send_email(message, mail_server_id, smtp_server, smtp_port,
                                      smtp_user, smtp_password, smtp_encryption, smtp_debug,
                                      smtp_session)
        else:
            message = "Email can't be send because local node and email nodes are different"
            _logger.error(message)
            raise Exception(message)
