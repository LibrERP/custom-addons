# © 2022-2023 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


from odoo import fields, models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def unlink(self):
        for invoice in self:
            if invoice.type in ('out_refund', 'in_invoice') and invoice.origin:
                for origin in invoice.origin.split(','):
                    picking = self.env['stock.picking'].search([('name', '=', origin.strip())])
                    if picking:
                        for move in picking.move_ids_without_package:
                            move.invoiced = False

            for picking in invoice.picking_ids:
                picking.invoice_state = '2binvoiced'

        return super().unlink()
