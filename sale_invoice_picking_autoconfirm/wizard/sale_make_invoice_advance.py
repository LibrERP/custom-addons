# © 2025-2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    confirm_picking = fields.Boolean('Confirm Picking', default=True)

    def create_invoices(self):
        order = self.env['sale.order'].browse(self.env.context.get('active_id'))
        if self.confirm_picking:
            order.validate_picking()
            order.message_post(body=_("La fattura è stata creata e l'uscita è stata convalidata"))
        else:
            order.message_post(body=_("La fattura è stata creata senza convalida di uscita"))

        return super().create_invoices()
