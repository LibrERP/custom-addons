# © 2022-2023 Andrei Levin <andrei.levin@didotech.com>
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
    journal_id = fields.Many2one('account.journal', string='Journal', required=True)
    type = fields.Selection(string='Type', selection=[
        ('sale', 'Refund'),
        ('purchase', 'Purchase')
    ], readonly=True)

    @api.model
    def default_get(self, defaults):
        results = super().default_get(defaults)
        picking = self.env['stock.picking'].browse(self._context['active_ids'][0])
        if picking.returned_by:
            results['type'] = 'sale'
        else:
            results['type'] = 'purchase'
            # results['journal_id'] = self.env.user.company_id.get_purchase_journal().id

        return results

    @api.multi
    def invoice_create_from_picking(self):
        invoice_line_model = self.env['account.invoice.line']
        invoice_model = self.env['account.invoice']

        partner = False
        moves_to_invoice = False
        names = []
        origin = []

        for count, picking in enumerate(self.picking_ids, start=1):
            if count == 1 and picking.returned_by:
                invoice_type = 'out_refund'
            elif count == 1:
                invoice_type = 'in_invoice'
            elif (picking.returned_by and invoice_type == 'in_invoice') \
                    or (not picking.returned_by and invoice_type == 'out_refund'):
                raise Warning(
                    _("All selected transfers should be of the same type Mixing of Refunds and Invoices is not permitted"))

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

            origin.append(picking.name)

        origin = ', '.join(origin)

        if not partner.property_account_receivable_id:
            raise Warning(_('No account defined for partner "%s".') % partner.name)

        name = ', '.join(names)

        if moves_to_invoice:
            addr = partner.address_get(['delivery', 'invoice'])

            invoice_values = {
                'name': name,
                'date_invoice': self.date_invoice,
                'type': invoice_type,
                'journal_id': self.journal_id.id,
                'partner_id': addr['invoice'] or partner.id,
                'currency_id': partner.currency_id.id,
                'fiscal_position_id': partner.property_account_position_id.id or False,
                'payment_term_id': partner.property_supplier_payment_term_id.id,
                'origin': origin
            }

            if invoice_type == 'in_invoice':
                invoice_values['account_id'] = partner.property_account_payable_id.id
            elif invoice_type == 'out_refund':
                invoice_values['account_id'] = partner.property_account_receivable_id.id
                if picking.sale_id:
                    invoice_values['payment_term_id'] = picking.sale_id.payment_term_id.id
                elif partner.property_payment_term_id:
                    invoice_values['payment_term_id'] = partner.property_payment_term_id.id
                else:
                    invoice_values['payment_term_id'] = False

            invoice = invoice_model.create(invoice_values)

            for picking in self.picking_ids:
                for move in picking.move_ids_without_package.filtered(lambda row: not row.invoiced):
                    if invoice_type == 'out_refund':
                        credit_account = move.product_id.property_account_income_id or move.product_id.categ_id.property_account_income_categ_id
                        if not credit_account:
                            msg = _('Default credit account is not set for the Product "{}".').format(move.product_id.name)
                            raise Warning(msg)
                    elif invoice_type == 'in_invoice':
                        debit_account = move.product_id.property_account_expense_id or move.product_id.categ_id.property_account_expense_categ_id
                        if not debit_account:
                            msg = _('Default debit account is not set for the Product "{}".').format(move.product_id.name)
                            raise Warning(msg)

                    values = {
                        'invoice_id': invoice.id,
                        'name': move.product_id.name,
                        'origin': picking.name,
                        'quantity': move.quantity_done,
                        'uom_id': move.product_uom.id,
                        'product_id': move.product_id and move.product_id.id or False
                    }
                    if invoice_type == 'in_invoice':
                        values['price_unit'] = move.purchase_line_id.price_unit or 0.0
                        values['invoice_line_tax_ids'] = [(6, 0, move.purchase_line_id.taxes_id.ids)]
                        values['discount'] = move.purchase_line_id and hasattr(move.purchase_line_id, 'discount') and move.purchase_line_id.discount or 0
                        values['account_id'] = debit_account.id
                    elif invoice_type == 'out_refund':
                        values['price_unit'] = move.sale_line_id and move.sale_line_id.price_unit or move.product_id.lst_price
                        values['invoice_line_tax_ids'] = move.sale_line_id and [(6, 0, move.sale_line_id.tax_id.ids)]
                        values['discount'] = move.sale_line_id and move.sale_line_id.discount or 0
                        if hasattr(partner, 'discount_class_id') and not values['discount']:
                            values['discount'] = partner.discount_class_id.percent or 0
                        values['account_id'] = credit_account.id

                    invoice_line = invoice_line_model.create(values)

                    if (invoice_type == 'in_invoice' and not move.purchase_line_id) or (invoice_type == 'out_refund' and not move.sale_line_id):
                        # Update price & taxes
                        invoice_line._compute_tax_id()
                        invoice_line.set_price_unit()

                    invoice_line._set_rc_flag(invoice)

                    # move.qty_invoiced += move.quantity_done
                    # if move.qty_invoiced == move.product_uom_qty:
                    move.invoiced = True
                    if move.purchase_line_id:  # Note di credito non hanno purchase lines
                        move.purchase_line_id.invoiced = True
                    # end if

                    move.invoice_line_ids = [(4, invoice_line.id)]

                if invoice_type == 'in_invoice':
                    for line in picking.purchase_id.order_line.filtered(lambda x: x.product_id.type == 'service' and not x.invoiced):
                        debit_account = line.product_id.property_account_expense_id
                        if not debit_account:
                            msg = _('Default debit account is not set for the Product "{}".').format(line.product_id.name)
                            raise Warning(msg)

                        values = {
                            'invoice_id': invoice.id,
                            'name': line.product_id.name,
                            'origin': picking.name,
                            'quantity': line.product_uom_qty,
                            'uom_id': line.product_uom.id,
                            'product_id': line.product_id and line.product_id.id or False,
                            'price_unit': line.price_unit or 0.0,
                            'invoice_line_tax_ids': [(6, 0, line.taxes_id.ids)],
                            'account_id': debit_account.id
                        }

                        invoice_line = invoice_line_model.create(values)
                        invoice_line._set_rc_flag(invoice)
                        line.invoiced = True

            invoice.compute_taxes()

            if invoice_type == 'out_refund':
                for picking in self.picking_ids:
                    picking.credit_note = invoice.id

            invoice.picking_ids = [(6, False, self.picking_ids.ids)]

            for picking_id in self.picking_ids:
                picking_id.invoice_state = 'invoiced'

            return invoice
        else:
            raise Warning(_('There are no lines that are not yet invoiced'))

    @api.multi
    def create_invoice(self):
        invoice = self.invoice_create_from_picking()
        ir_model_data = self.env['ir.model.data']

        if invoice.type == 'in_invoice':
            form_res = ir_model_data.get_object_reference(
                'account',
                'invoice_supplier_form')
            tree_res = ir_model_data.get_object_reference(
                'account',
                'invoice_supplier_tree')

        elif invoice.type == 'out_refund':
            form_res = ir_model_data.get_object_reference(
                'account',
                'invoice_form')
            tree_res = ir_model_data.get_object_reference(
                'account',
                'invoice_tree')

        form_id = form_res and form_res[1] or False
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
