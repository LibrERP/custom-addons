# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models
from odoo.exceptions import UserError


class FatturapaAttachmentOut(models.Model):
    _inherit = "fatturapa.attachment.out"

    # def write(self, values):
    #     if 'datas' in values and not values.get('datas'):
    #         values['name'] = 'deleted'
    #
    #     super().write(values)
    #
    #     if 'datas' in values and not values.get('datas'):
    #         self.unlink()

    def unlink(self):
        for attachment_out in self:
            if attachment_out.state == "sender_error":
                attachment_out.state = "ready"

        return super().unlink()
