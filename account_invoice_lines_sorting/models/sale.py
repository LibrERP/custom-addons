#    Copyright (C) 2023 Didotech srl (<https://www.didotech.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Sale(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        order = super().create(vals)
        if order.order_line:
            order.update_sequence()
        return order

    def update_sequence(self):
        if self.order_line:
            sequences = set(self.order_line.mapped('sequence'))
            if len(sequences) == 1:
                counter = 0
                for line in self.order_line:
                    seq = line.sequence
                    line.write({
                        'sequence': seq + counter
                    })
                    counter += 1

    @api.multi
    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            order.update_sequence()

        return res


    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        """Create invoice note lines with notes from the sale order"""
        invoice_ids = super().action_invoice_create(
            grouped=grouped, final=final
        )

        for inv_id in invoice_ids:
            inv = self.env['account.invoice'].browse(inv_id)
            if inv.invoice_line_ids:
                for line in inv.invoice_line_ids:
                    if line.sale_line_ids and line.sale_line_ids[0].sequence:
                        line.write({
                            'sequence': line.sale_line_ids[0].sequence
                        })

        if self.env.context.get('_copy_notes'):
            note_lines_vals = []
            for sale_order in self:
                invoice = sale_order.invoice_ids.filtered(
                    lambda i: i.id in invoice_ids
                )
                if not invoice:
                    # The sale order did not generate an invoice
                    continue
                notes_to_create = sale_order.order_line.filtered(
                    lambda l: l.display_type == 'line_note'
                )
                for note in notes_to_create:
                    note_vals = {
                        'origin': sale_order.name,
                        'invoice_id': invoice.id,
                        'sequence': note.sequence,
                        'display_type': 'line_note',
                        'name': note.name
                    }
                    note_lines_vals.append(note_vals)
            self.env['account.invoice.line'].create(note_lines_vals)
        return invoice_ids

