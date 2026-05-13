from odoo import _, models
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_open_move_import(self):
        self.ensure_one()

        if self.state in ("done", "cancel"):
            raise UserError(_("You can only import moves on a transfer that is not done or cancelled."))

        return {
            "type": "ir.actions.client",
            "tag": "import",
            "name": _("Import Stock Moves"),
            "params": {
                "active_model": "stock.move",
                "context": {
                    "active_id": self.id,
                    "active_model": "stock.picking",
                    "default_picking_id": self.id,
                    "default_company_id": self.company_id.id,
                },
            },
        }
