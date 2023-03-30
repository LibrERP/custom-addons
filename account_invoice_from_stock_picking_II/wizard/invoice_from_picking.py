# © 2022-2023 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models, api, _
from odoo.exceptions import Warning
from odoo.addons import decimal_precision as dp


class InvoiceFromPickings(models.TransientModel):
    _name = "invoice.from.pickings"
    _description = 'Invoice from pickings'

    def _get_picking_ids(self):
        return self.env['stock.picking'].browse(
            self.env.context['active_ids']
        ).filtered(lambda row: row.picking_type_id.code == 'incoming')

    def _get_future_lines(self):
        stock_moves = self.env['stock.move'].search([
            ('picking_id', 'in', self.env.context['active_ids']),
            ('invoiced', '=', False)
        ])

        picking = self.env['stock.picking'].browse(self._context['active_id'])

        if picking.returned_by:
            invoice_type = 'out_refund'
        else:
            invoice_type = 'in_invoice'

        invoice_lines = self.env['invoice.from.picking.line']
        for move in stock_moves:
            values = {
                'picking_line_id': move.id,
            }

            if invoice_type == 'in_invoice':
                values['unit_price'] = move.purchase_line_id and move.purchase_line_id.price_unit or 0.0
                if move.purchase_line_id and hasattr(move.purchase_line_id, 'discount'):
                    values['discount'] = move.purchase_line_id and move.purchase_line_id.discount or 0
                else:
                    values['discount'] = 0
            else:
                values['unit_price'] = move.sale_line_id and move.sale_line_id.price_unit or move.product_id.lst_price
                values['discount'] = move.sale_line_id and move.sale_line_id.discount or 0

            if move.purchase_line_id and hasattr(move.purchase_line_id, 'discount'):
                values['discount'] = move.purchase_line_id and move.purchase_line_id.discount or 0
            else:
                values['discount'] = 0

            values['total_amount'] = move.quantity_done * values['unit_price'] * (1 - values['discount'] / 100)

            invoice_lines += self.env['invoice.from.picking.line'].create(values)
        return invoice_lines

    def _get_partner(self):
        if 'active_ids' in self.env.context:
            picking = self.env['stock.picking'].browse(self.env.context['active_ids'][0])
            return picking.partner_id
        else:
            return False

    picking_ids = fields.Many2many(
        'stock.picking', default=_get_picking_ids
    )
    future_invoice_line_ids = fields.One2many(
        comodel_name="invoice.from.picking.line",
        string="Invoice Lines",
        required=False,
        default=_get_future_lines,
        inverse_name="wizard_id"
    )
    date_invoice = fields.Date(string='Bill Date', required=True)
    journal_id = fields.Many2one('account.journal', string='Journal', required=True)
    type = fields.Selection(string='Type', selection=[
        ('sale', 'Refund'),
        ('purchase', 'Purchase')
    ], readonly=True)
    invoice_id = fields.Many2one('account.invoice', string='Invoice')
    partner_id = fields.Many2one('res.partner', string='Partner', required=False, default=_get_partner, readonly=False)

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

        if not partner.property_account_receivable_id:
            raise Warning(_('No account defined for partner "%s".') % partner.name)

        name = ', '.join(names)

        if moves_to_invoice:
            if self.invoice_id:
                invoice = self.invoice_id
                invoice_origin = invoice.origin and invoice.origin.split(',') or []
                invoice_origin = [name.strip() for name in invoice_origin]
                origin = invoice_origin + origin
                origin = list(set(origin))
                invoice.origin = ', '.join(origin)
            else:
                addr = self.partner_id.address_get(['delivery', 'invoice'])

                invoice_values = {
                    'name': name,
                    'date_invoice': self.date_invoice,
                    'type': invoice_type,
                    'journal_id': self.journal_id.id,
                    'partner_id': addr['invoice'] or self.partner_id.id,
                    'currency_id': partner.currency_id.id,
                    'fiscal_position_id': partner.property_account_position_id.id or False,
                    'payment_term_id': partner.property_supplier_payment_term_id.id,
                    'origin': ', '.join(origin)
                }

                if invoice_type == 'in_invoice':
                    invoice_values['account_id'] = partner.property_account_payable_id.id
                elif invoice_type == 'out_refund':
                    invoice_values['account_id'] = partner.property_account_receivable_id.id
                    invoice_values['payment_term_id'] = picking.sale_id and picking.sale_id.payment_term_id.id or False

                invoice = invoice_model.create(invoice_values)

            for future_line in self.future_invoice_line_ids:
                move = future_line.picking_line_id
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
                    'product_id': move.product_id and move.product_id.id or False,
                    'price_unit': future_line.unit_price or 0.0,
                    'discount': future_line.discount
                }

                if invoice_type == 'in_invoice':
                    # values['price_unit'] = move.purchase_line_id.price_unit or 0.0
                    values['invoice_line_tax_ids'] = [(6, 0, move.purchase_line_id.taxes_id.ids)]
                    # values['discount'] = move.purchase_line_id and hasattr(move.purchase_line_id, 'discount') and move.purchase_line_id.discount or 0
                    values['account_id'] = debit_account.id
                elif invoice_type == 'out_refund':
                    # values['price_unit'] = move.sale_line_id and move.sale_line_id.price_unit or move.product_id.lst_price
                    values['invoice_line_tax_ids'] = move.sale_line_id and [(6, 0, move.sale_line_id.tax_id.ids)]
                    # values['discount'] = move.sale_line_id and move.sale_line_id.discount or 0
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

            for picking in self.picking_ids:
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

            if self.invoice_id:
                picking_ids = self.invoice_id.picking_ids + self.picking_ids
            else:
                picking_ids = self.picking_ids

            invoice.picking_ids = [(6, False, picking_ids.ids)]

            for picking in self.picking_ids:
                picking.invoice_state = 'invoiced'

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

    @api.onchange('invoice_id')
    def onchage_invoice_id(self):
        if self.invoice_id:
            self.partner_id = self.invoice_id.partner_id
            self.journal_id = self.invoice_id.journal_id
            self.date_invoice = self.invoice_id.date_invoice


class InvoiceFromPickingLine(models.TransientModel):
    _name = "invoice.from.picking.line"
    _description = 'Invoice from picking line'

    wizard_id = fields.Many2one(comodel_name='invoice.from.pickings', string="Wizard", required=False)
    picking_line_id = fields.Many2one(comodel_name='stock.move', string="Invoice Lines", required=False)
    product_id = fields.Many2one(related='picking_line_id.product_id', string='Product', readonly=True)
    product_qty = fields.Float(related='picking_line_id.quantity_done', string='Quantity', readonly=True)
    unit_price = fields.Float("Unit Price", digits=dp.get_precision('Purchase Price'))
    discount = fields.Float("Discount", default=0)
    total_amount = fields.Float(digits=dp.get_precision('Purchase Price'), string="Total Price", readonly=True)

    @api.onchange('unit_price', 'product_qty', 'discount')
    def recalculate_total_amount(self):
        self.total_amount = self.product_qty * self.unit_price * (1 - self.discount / 100)
