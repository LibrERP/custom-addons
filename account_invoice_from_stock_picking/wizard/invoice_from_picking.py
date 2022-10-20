# © 2022 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models, api, _
from odoo.exceptions import Warning


class InvoiceFromPickings(models.TransientModel):
    _name = "invoice.from.pickings"
    _description = 'Invoice from pickings'

    def _get_picking_ids(self):
        return self.env['stock.picking'].browse(
            self.env.context['active_ids']
        ).filtered(lambda row: row.picking_type_id.code == 'incoming')

    picking_ids = fields.Many2many(
        'stock.picking', default=_get_picking_ids
    )
    date_invoice = fields.Date(string='Bill Date', required=True)
    journal_id = fields.Many2one('account.journal', string='Journal')

    @api.model
    def default_get(self, defaults):
        results = super().default_get(defaults)
        results['journal_id'] = self.env.user.company_id.get_purchase_journal().id
        return results

    @api.multi
    def invoice_create_from_picking(self):
        invoice_line_model = self.env['account.invoice.line']
        invoice_model = self.env['account.invoice']

        partner = False
        moves_to_invoice = False
        names = []

        for picking in self.picking_ids:
            current_partner = picking.partner_id
            if partner and partner.id != current_partner.id:
                raise Warning(
                    _("Selected Pickings have different Partner"))
            elif not partner:
                partner = current_partner

            if picking.move_ids_without_package.filtered(lambda row: not row.invoiced):
                moves_to_invoice = True

            if picking.ddt_supplier_number:
                names.append(picking.ddt_supplier_number)

        if not partner.property_account_receivable_id:
            raise Warning(_('No account defined for partner "%s".') % partner.name)

        name = ', '.join(names)

        if moves_to_invoice:
            addr = partner.address_get(['delivery', 'invoice'])

            credit_account = self.journal_id.default_credit_account_id

            invoice = invoice_model.create({
                'name': name,
                'date_invoice': self.date_invoice,
                'type': 'in_invoice',
                'account_id': partner.property_account_payable_id.id,
                'journal_id': self.journal_id.id,
                'partner_id': addr['invoice'] or partner.id,
                'currency_id': partner.currency_id.id,
                'fiscal_position_id': partner.property_account_position_id.id or False,
                'payment_term_id': partner.property_supplier_payment_term_id.id
            })

            for picking in self.picking_ids:
                for move in picking.move_ids_without_package.filtered(lambda row: not row.invoiced):
                    invoice_line = invoice_line_model.create({
                        'invoice_id': invoice.id,
                        'name': move.product_id.name,
                        'origin': picking.name,
                        'account_id': credit_account.id,
                        'quantity': move.quantity_done,
                        'invoice_line_tax_ids': [(6, 0, move.purchase_line_id.taxes_id.ids)],
                        'uom_id': move.product_uom.id,
                        'price_unit': move.purchase_line_id.price_unit or 0.0,
                        'product_id': move.product_id and move.product_id.id or False
                    })

                    if not move.purchase_line_id:
                        # Update price & taxes
                        invoice_line._compute_tax_id()
                        invoice_line.set_price_unit()

                    move.qty_invoiced += move.quantity_done
                    if move.qty_invoiced == move.product_uom_qty:
                        move.invoiced = True
                    move.invoice_line_ids = [(4, invoice_line.id)]

            invoice.compute_taxes()

            return invoice
        else:
            raise Warning(_('There are no lines that are not yet invoiced'))

    @api.multi
    def create_invoice(self):
        invoice = self.invoice_create_from_picking()

        ir_model_data = self.env['ir.model.data']
        form_res = ir_model_data.get_object_reference(
            'account',
            'invoice_supplier_form')
        form_id = form_res and form_res[1] or False
        tree_res = ir_model_data.get_object_reference(
            'account',
            'invoice_supplier_tree')
        tree_id = tree_res and tree_res[1] or False
        return {
            'name': _('INV'),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'account.invoice',
            'res_id': invoice.id,
            'view_id': False,
            'views': [(form_id, 'form'), (tree_id, 'tree')],
            'type': 'ir.actions.act_window',
        }
