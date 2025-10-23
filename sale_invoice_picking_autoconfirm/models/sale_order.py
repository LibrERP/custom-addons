# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def validate_picking(self):
        for order in self:
            for picking in order.picking_ids:
                # check lot number is correct
                if picking.lot_numbers_match():
                    picking.action_set_quantities_to_reservation()
                    picking.button_validate()
                else:
                    order.message_post(
                        body=_("""⚠️ <strong>Lot Numbers Mismatch</strong><br/>
            The lot numbers in the picking do not match the sale order lines."""),
                        message_type='notification',
                        subtype_xmlid='mail.mt_comment'
                    )

        return True
