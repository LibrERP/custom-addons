# Copyright 2020 Andrei Levin - Didotech srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.onchange('partner_id')
    def need_reference(self):
        if self.partner_id and self.partner_id.require_po_reference:
            self.reference_required = True
        else:
            self.reference_required = self.partner_id and self.partner_id.xml_dialect in ('amazon',) or False

    reference_required = fields.Boolean(compute=need_reference, string="Reference required")
    customer_reference = fields.Char(string="Customer Order", help="Customer PO reference")
