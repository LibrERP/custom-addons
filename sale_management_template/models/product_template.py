# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    selected_in_template = fields.Boolean('Selected in template')
