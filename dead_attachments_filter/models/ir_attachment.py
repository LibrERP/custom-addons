# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import os

from odoo import api, models
from odoo.osv import expression


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        domain = list(args)

        marker = ("id", "in", "missing_attachments")

        if any(tuple(term) == marker for term in domain):
            base = self._filestore()
            # Mentioning res_field in the domain disables core ir.attachment's
            # implicit ('res_field', '=', False) filter (see
            # base/models/ir_attachment.py::_search), so field-backed
            # attachments (images, web icons, stored reports, ...) are scanned
            # too — these are the ones that usually spam the log with missing
            # file errors.
            attachments = self.search([
                "|", ("res_field", "=", False), ("res_field", "!=", False),
                ("store_fname", "!=", False),
            ])

            missing_ids = attachments.filtered(
                lambda a: not os.path.exists(
                    os.path.join(base, a.store_fname)
                )
            ).ids

            domain = expression.AND([
                [("id", "in", missing_ids)],
                [
                    term for term in domain
                    if tuple(term) != marker
                ],
            ])

        return super()._search(
            domain,
            offset=offset,
            limit=limit,
            order=order,
            access_rights_uid=access_rights_uid,
        )
