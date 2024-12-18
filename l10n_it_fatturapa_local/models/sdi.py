# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models
from odoo.exceptions import UserError
import os
import base64


class SdiChannel(models.Model):
    _inherit = "sdi.channel"

    channel_type = fields.Selection(
        selection_add=[("local", "Local Folder")],
        ondelete={"local": "cascade"}
    )

    destination_path = fields.Char(
        string="Path to destination"
    )

    def send_via_local(self, attachment_out_ids: list[models.Model]) -> None:
        for att in attachment_out_ids:
            if not att.datas or not att.name:
                raise UserError(_("File content and file name are mandatory"))
            else:
                file_path = os.path.join(self.destination_path, att.name)
                with open(file_path, 'wb') as invoice:
                    invoice.write(base64.b64decode(att.datas))
                att.message_post(
                    body=f"File {att.name} salvato in {self.destination_path}")
                att.state = "sent"
                att.sending_date = fields.Datetime.now()
                att.sending_user = self.env.user.id
