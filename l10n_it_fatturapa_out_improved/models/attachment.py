# -*- coding: utf-8 -*-
# © 2021 Andrei Levin - Didotech srl (www.didotech.com)

from odoo import fields, models, api, _


class UnlinkControlMixin(models.AbstractModel):
    _name = 'unlink.control.mixin'

    def unlink(self):
        for attachment_out in self:
            if attachment_out.state == 'sender_error':
                attachment_out.state = 'ready'

        return super().unlink()


class FatturaPAAttachment(models.Model):
    _name = "fatturapa.attachment.out"
    _inherit = [
        'unlink.control.mixin',
        "fatturapa.attachment.out",
    ]

    def _get_invoice_names(self):
        for attachment in self:
            attachment.invoices = ', '.join(
                [invoice.number or '*' for invoice in attachment.out_invoice_ids if invoice]
            )

    invoices = fields.Char(
        string="Invoices", required=False, compute=_get_invoice_names
    )
