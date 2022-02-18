# © 2016-2022 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, _


class ProductProduct(models.Model):
    _inherit = "product.product"

    description = fields.Text(
        _('Description'), translate=True,
        help=_("A precise description of the Product, used only for internal information purposes.")
    )
