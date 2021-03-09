# -*- coding: utf-8 -*-
# © 2021 Andrei Levin - Didotech srl (www.didotech.com)

from odoo import fields, models, api, _


class FatturaPAAttachment(models.Model):
    _inherit = "fatturapa.attachment.out"

    def _get_invoice_names(self):
        for attachment in self:
            attachment.invoices = ', '.join(
                [invoice.number or '*' for invoice in attachment.out_invoice_ids if invoice]
            )

    invoices = fields.Char(
        string="Invoices", required=False, compute=_get_invoice_names, store=True
    )
