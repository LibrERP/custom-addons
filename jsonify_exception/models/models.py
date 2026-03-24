# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models
from odoo.exceptions import UserError


class Base(models.AbstractModel):
    _inherit = "base"

    def _jsonify_record_handle_function(self, rec, field_dict, strict):
        field_name = field_dict["name"]
        function = field_dict["function"]
        return self._function_value(rec, function, field_name)
