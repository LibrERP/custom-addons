# © 2022 Marco Tosato <marco.tosato@didotech.com>
# © 2022 Didotech SRL <info@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def name_get(self):

        standard_names = super().name_get()

        shortened_names = list()

        for inv_id, inv_name in standard_names:
            if inv_name and len(inv_name) > 90:
                short_name = inv_name[:90] + ' ...'
            else:
                short_name = inv_name
            # end if

            shortened_names.append(
                (inv_id, short_name)
            )
        # end for

        return shortened_names
    # end name_get
# end AccountInvoice


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    def _get_anglo_saxon_price_unit(self):
        price_unit = super(AccountInvoiceLine, self)._get_anglo_saxon_price_unit()
        if self.product_id._get_invoice_policy() == "delivery" and self.env.context.get("pos_picking_id"):
            moves = (
                self.env.context["pos_picking_id"]
                .move_lines.filtered(lambda m: m.product_id == self.product_id)
                .sorted(lambda x: x.date)
            )
            quantity = self.uom_id._compute_quantity(self.quantity, self.product_id.uom_id)
            average_price_unit = self.product_id._compute_average_price(0.0, quantity, moves)
            price_unit = average_price_unit or price_unit
            price_unit = self.product_id.uom_id._compute_price(price_unit, self.uom_id)

        return price_unit
