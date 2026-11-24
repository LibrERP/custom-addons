# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models

SOL_EDITABLE_FORM = 'sale_project.sale_order_line_view_form_editable'


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def default_get(self, fields):
        """Reuse an empty quotation instead of creating a new one each time.

        sale_project's ``default_get`` creates (and commits) a new quotation
        for ``default_partner_id`` every time the editable SOL form opens
        without an order, so each opened-and-discarded "Create and edit"
        dialog leaves an empty draft quotation behind and burns a number.
        Offer the latest empty draft quotation of the same user, customer and
        company as the default order, so sale_project keeps it instead of
        creating another one. The ``link_to_project`` flow is left untouched,
        as it links the new quotation to a project.
        """
        ctx = self.env.context
        if (
            ctx.get('form_view_ref') == SOL_EDITABLE_FORM
            and 'order_id' in fields
            and ctx.get('default_partner_id')
            and not ctx.get('default_order_id')
            and not ctx.get('link_to_project')
        ):
            order = self._get_reusable_empty_order()
            if order:
                self = self.with_context(default_order_id=order.id)
        return super(SaleOrderLine, self).default_get(fields)

    @api.model
    def _get_reusable_empty_order(self):
        # Same partner/company sale_project would use to create the order.
        ctx = self.env.context
        return self.env['sale.order'].search([
            ('state', '=', 'draft'),
            ('partner_id', '=', ctx['default_partner_id']),
            ('company_id', '=', ctx.get('company_id') or self.env.company.id),
            ('create_uid', '=', self.env.uid),
            ('order_line', '=', False),
        ], order='id desc', limit=1)

    @api.model
    def _add_missing_default_values(self, values):
        """Keep the description the user typed in the SOL dialog.

        sale_project drops ``name`` from the result whenever ``product_id`` is
        present and the editable SOL form is used (helpdesk ticket / task
        "Sales Order Item" field). It means to discard only the text typed in
        a quick-create (``name_create``), but the base method returns the
        given values merged with defaults, so it also discards a description
        typed explicitly in the "Create and edit" dialog. The line then gets
        the product's sales description instead.

        Restore ``name`` when the caller provided it, except for the
        quick-create path, which sale_project marks with ``sol_product_name``.
        """
        defaults = super()._add_missing_default_values(values)
        if (
            self.env.context.get('form_view_ref') == SOL_EDITABLE_FORM
            and values.get('name')
            and 'name' not in defaults
            and not self.env.context.get('sol_product_name')
        ):
            defaults['name'] = values['name']
        return defaults
