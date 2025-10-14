# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models
from odoo.exceptions import UserError


class StockDeliveryNote(models.Model):
    _inherit = "stock.delivery.note"

    def _check_delivery_notes_before_invoicing(self):
        # !!! Attention !!!
        # This function overrides function from l10n_it_delivery_note module
        #removing the invoicing policy related code
        for delivery_note_id in self:
            if not delivery_note_id.sale_ids:
                raise UserError(
                    _("%s hasn't sale order!") % delivery_note_id.display_name
                )
            if "incoming" in delivery_note_id.mapped(
                "sale_ids.picking_ids.picking_type_id.code"
            ):
                raise UserError(
                    _(
                        "Sale orders related to %s have return! "
                        "For invoicing, go to sale orders."
                    )
                    % delivery_note_id.display_name
                )
            if delivery_note_id.invoice_status == "invoiced":
                raise UserError(
                    _("%s is already invoiced!") % delivery_note_id.display_name
                )
            if delivery_note_id.state == "draft":
                raise UserError(_("%s is in draft!") % delivery_note_id.display_name)
