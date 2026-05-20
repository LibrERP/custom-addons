# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    l10n_it_supplier_ddt_number = fields.Char(
        string="Supplier DDT Number",
        tracking=True,
        copy=False,
        help="DDT number issued by the supplier and reported on the goods received.",
    )
    l10n_it_supplier_ddt_date = fields.Date(
        string="Supplier DDT Date",
        tracking=True,
        copy=False,
    )