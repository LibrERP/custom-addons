# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _


class DdtCreateInvoice(models.TransientModel):
    _inherit = "ddt.create.invoice"
    _description = "Create invoice from TD"

    @api.multi
    def create_invoice(self):
        if self.ddt_ids:
            self.ddt_ids = self.ddt_ids.sorted(key=lambda x: x.date)
            return super().create_invoice()

# class StockPickingPackagePreparation(models.Model):
#
#     _inherit = 'stock.picking.package.preparation'
#
#     @api.multi
#     def action_invoice_create(self):
#         print(self)
#         print(len(self))
#         return super().action_invoice_create()


