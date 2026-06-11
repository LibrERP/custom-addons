# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class AtecoCategory(models.Model):
    _inherit = "ateco.category"

    macro_category_name = fields.Char(
        compute='_get_macro_category_name',
        store=True,
    )
    active = fields.Boolean(default=True)
    search_code = fields.Char(
        string="Code",
        compute='_compute_search_helpers',
        search='_search_code_starts_with',
    )
    search_name = fields.Char(
        string="Name",
        compute='_compute_search_helpers',
        search='_search_name_starts_with',
    )

    @api.depends('parent_id.macro_category_name', 'code', 'name')
    def _get_macro_category_name(self):
        for category in self:
            category.macro_category_name = category.parent_id and category.get_macro_category() or ''

    def get_macro_category(self):
        self.ensure_one()

        if self.parent_id:
            return self.parent_id.get_macro_category()
        else:
            return self.code + ' - ' + self.name

    def _compute_search_helpers(self):
        for rec in self:
            rec.search_code = False
            rec.search_name = False

    def _search_code_starts_with(self, operator, value):
        return self._search_starts_with_children('code', value)

    def _search_name_starts_with(self, operator, value):
        return self._search_starts_with_children('name', value)

    def _search_starts_with_children(self, field_name, value):
        pattern = (value or '') + '%'
        matches = self.with_context(active_test=False).search(
            [(field_name, '=ilike', pattern)]
        )
        if not matches:
            return [('id', '=', 0)]
        return [('id', 'child_of', matches.ids)]
