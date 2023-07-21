# Copyright 2023 Didotech (https://www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class DdtCreditNote(models.TransientModel):
    _name = "ddt.credit.note"
    _description = "Credit Note TD"

    @api.model
    def _default_journal(self):
        return self.env['account.journal'].search([('type', '=', 'purchase')],
                                                  order='id', limit=1)
    journal_id = fields.Many2one('account.journal', string='Journal',
                                 default=_default_journal,
                                 required=True,
                                 domain=[('type', '=', 'purchase')])
    date_invoice = fields.Date(
        string='Invoice Date',
        required=True,
    )

    def create_credit_note(self):
        # print(self._context)
        def get_picking_by_product(sppp, product_id):
            sp = sppp.picking_ids.filtered(lambda s: s.product_id.id == product_id)
            if len(sp) == 1 and sp.group_id:
                whin = self.env['stock.picking'].search([
                    ('group_id', '=', sp.group_id.id),
                    ('partner_id', '=', sppp.partner_id.id),
                    ('picking_type_code', '=', 'incoming'),
                    ('product_id', '=', product_id),
                ])
                if len(whin) == 1:
                    return whin
            return False

        active_id = self._context.get('active_id')
        stock_preparation = self.env['stock.picking.package.preparation'].browse(active_id)
        if stock_preparation.transportation_reason_id.return_supplier is False:
            raise UserError('Non è possibile creare una nota di credito per questo tipo di DDT.')

        values = dict()
        values['type'] = 'in_refund'
        values['date_invoice'] = self.date_invoice
        values['journal_id'] = self.journal_id.id
        values['date_due'] = values['date_invoice']
        values['state'] = 'draft'
        values['number'] = False
        values['origin'] = stock_preparation.ddt_number or False
        values['refund_invoice_id'] = False
        values['reference'] = False
        values['payment_term_id'] = stock_preparation.partner_id.property_supplier_payment_term_id.id or False
        values['account_id'] = (
            stock_preparation.partner_id.property_account_payable_id.id)
        values['partner_id'] = stock_preparation.partner_id.id
        values['currency_id'] = stock_preparation.partner_id.currency_id.id
        values['invoice_line_ids'] = []

        # invoice lines
        for line in stock_preparation.line_ids:
            price = 0.0
            qty = line.product_uom_qty
            tax = line.product_id.taxes_id or False
            product = line.product_id
            account = product.property_account_expense_id or product.categ_id.property_account_expense_categ_id
            stock_in = get_picking_by_product(stock_preparation, product.id)
            if stock_in and stock_in.origin:
                po = self.env['purchase.order'].search([('name', '=', stock_in.origin)])
                if po:
                    po_line = po.order_line.filtered(lambda x: x.product_id.id == product.id)
                    if len(po_line) == 1:
                        price = po_line.price_unit
                        tax = po_line.taxes_id or False
            else:
                if product.seller_ids:
                    supinfos_sorted = product.seller_ids.sorted(key=lambda r: r.sequence)
                    supinfos = supinfos_sorted.filtered(
                        lambda x: x.name.id == stock_preparation.partner_id.id)
                    if supinfos:
                        supinfo = supinfos[0]
                        if line.product_uom_qty >= supinfo.min_qty:
                            price = supinfo.price
            res = {
                'name': product.name,
                'sequence': 10,
                'origin': values['origin'],
                'account_id': account and account.id or False,
                'quantity': qty,
                'price_unit': price,
                'uom_id': product.uom_id.id,
                'product_id': product.id or False,
                # 'invoice_id': invoice_refund.id,
            }
            if tax:
                res['invoice_line_tax_ids'] = (6, 0, tax.ids),

            values['invoice_line_ids'].append((0, 0, res))

        invoice_refund = self.env['account.invoice'].create(values)

            # self.env['account.invoice.line'].create(res)

        # invoice_refund.compute_taxes()
        # update ddt with credit note
        stock_preparation.write({
            'invoice_id': invoice_refund.id
        })

        # show credit note
        ir_model_data = self.env['ir.model.data']
        form_res = ir_model_data.get_object_reference(
            'account', 'invoice_form')
        form_id = form_res and form_res[1] or False
        tree_res = ir_model_data.get_object_reference(
            'account', 'invoice_tree')
        tree_id = tree_res and tree_res[1] or False
        return {
            'name': _('Credit Note from TD'),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'account.invoice',
            'domain': [('id', 'in', [invoice_refund.id])],
            'view_id': False,
            'views': [(tree_id, 'tree'), (form_id, 'form')],
            'type': 'ir.actions.act_window',
        }



