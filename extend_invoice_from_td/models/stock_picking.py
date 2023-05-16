##############################################################################
#
#    Copyright (C) 2022 Didotech SRL
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp

from odoo.fields import first
from odoo.tools.float_utils import float_is_zero
from odoo.tools.misc import formatLang, format_date


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    credit_note = fields.Many2one(
        'account.invoice',
        string='Credit note',
        readonly=True
    )

    # returned_by = fields.Boolean(
    #     string='Returned by customer',
    #     default=False,
    # )

    main_partner = fields.Many2one(
        'res.partner',
        string='Partner principale',
        compute='_compute_main_partner',
        store=True,
    )

    @api.depends('partner_id')
    def _compute_main_partner(self):
        for sp in self:
            if sp.returned_by and sp.move_lines and sp.move_lines.filtered(lambda l: l.sale_line_id):
                line_ids = sp.move_lines.filtered(lambda l: l.sale_line_id)
                order = line_ids[0].sale_line_id.order_id
                if order.partner_invoice_id.id != order.partner_id.id:
                    partner = order.partner_invoice_id
                else:
                    partner = order.partner_id
            elif sp.partner_id.parent_id:
                partner = sp.partner_id.parent_id
            else:
                partner = sp.partner_id

            sp.main_partner = partner

    @api.multi
    def action_invoice_refund(self):
        #
        grouped_invoices, references = self.create_td_grouped_invoices()
        if not grouped_invoices:
            raise UserError(_('There is no invoiceable line.'))

        journal_id = self._context.get('refund_journal_id', False)
        for invoice in list(grouped_invoices.values()):
            if not invoice.name:
                invoice.update({
                    'name': invoice.origin,
                })

            if journal_id:
                invoice.update({
                    'journal_id': journal_id
                })

        # return [inv.id for inv in list(grouped_invoices.values())]

    @api.multi
    def action_invoice_refund_wcontext(self, cntx=None):
        # set context if any
        if cntx:
            self = self.with_context(cntx)
        self.action_invoice_refund()

    @api.multi
    def create_td_grouped_invoices(self):
        """
        Create the invoices, grouped by `group_key` (see `get_td_group_key`).
        :return: (
            dictionary group_key -> invoice record-set,
            dictionary invoice -> TD record-set,
            )
        """
        inv_obj = self.env['account.invoice']
        grouped_invoices = {}
        references = {}
        for sp in self:
            if not sp.returned_by or sp.credit_note:
                continue

            group_key = sp.get_td_group_key()
            if group_key not in grouped_invoices:
                inv_data = sp._prepare_invoice()
                grouped_invoices[group_key] = inv_obj.create(inv_data)

            invoice = grouped_invoices.get(group_key)
            sp.credit_note = invoice.id

            if invoice not in references:
                references[invoice] = sp
            else:
                references[invoice] |= sp

            for line in sp.move_lines:
                if line.product_uom_qty > 0:
                    line.invoice_line_create(invoice, line.product_uom_qty)

            origin = invoice.origin
            if origin and sp.name not in origin.split(', '):
                invoice.update({
                    'origin': origin + ', ' + sp.name
                })

        return grouped_invoices, references

    @api.multi
    def _prepare_invoice(self):

        self.ensure_one()
        res = {
            'type': 'out_refund',
            'company_id': self.company_id.id
        }
        journal_id = self._context.get('refund_journal_id', False)

        if not journal_id:
            raise UserError(
                'Registro per movimenti per note di credito non impostato.'
            )
        journal = self.env['account.journal'].browse(journal_id)

        invoice_partner_id = self.main_partner.id
        invoice_partner = self.main_partner

        invoice_description = '' # self._prepare_invoice_description()
        currency_id = journal.currency_id.id or journal.company_id.currency_id.id

        if self.payment_term_id and self.payment_term_id.id:
            payment_term_id = self.payment_term_id.id
        else:
            if self.main_partner.property_payment_term_id and self.main_partner.property_payment_term_id.id:
                payment_term_id = self.main_partner.property_payment_term_id.id
            else:
                payment_term_id = None

        fiscal_position_id = None

        res.update({
            'name': invoice_description or '',
            'origin': self.name,
            'date_invoice': self._context.get('invoice_date', False),
            'account_id': (
                invoice_partner.property_account_receivable_id.id),
            'partner_id': invoice_partner_id,
            'journal_id': journal_id,
            'currency_id': currency_id,
            'fiscal_position_id': fiscal_position_id,
            'payment_term_id': payment_term_id
        })
        return res

    # def get_td_group_key(self):
    #     """
    #     if group into context is False group_key is the TD id
    #     which makes one invoice per td
    #     """
    #
    #     self.ensure_one()
    #
    #     has_group = self._context.get('group', True)
    #
    #     if has_group is True:
    #         partner = self._get_partner()
    #         billing_partner = self._get_billing_partner()
    #         shipping_partner = self._get_shipping_partner()
    #
    #         if partner.ddt_invoicing_group and partner.ddt_invoicing_group == 'shipping_partner':
    #             group_method = 'shipping_partner'
    #         else:
    #             group_method = 'billing_partner'
    #
    #         group_key = ''
    #         if group_method == 'billing_partner':
    #             group_key = (billing_partner.id,
    #                          billing_partner_id.currency_id.id)
    #         elif group_method == 'shipping_partner':
    #             group_key = (shipping_partner.id,
    #                          shipping_partner.currency_id.id)
    #         elif group_method == 'nothing':
    #             group_key = self.id
    #         return group_key
    #     else:
    #         group_key = self.id
    #     # end if
    #
    #     return group_key

    def get_td_group_key(self):

        has_group = self._context.get('group', True)

        if has_group is True:

            order = self._get_sale_order_ref()
            if order:
                group_method = order.ddt_invoicing_group or 'shipping_partner'
                group_partner_invoice_id = order.partner_invoice_id.id
                group_currency_id = order.currency_id.id
            else:
                group_method = self.partner_id.parent_id.ddt_invoicing_group or self.partner_id.ddt_invoicing_group
                group_partner_invoice_id = self.partner_id.id
                group_currency_id = self.partner_id.currency_id.id

            group_key = ''
            if group_method == 'billing_partner':
                group_key = (group_partner_invoice_id,
                             group_currency_id)
            elif group_method == 'shipping_partner':
                group_key = (self.partner_id.id,
                             self.company_id.currency_id.id)
            elif group_method == 'code_group':
                partner = self.partner_id.parent_id or self.partner_id
                group_key = (self.partner_id.ddt_code_group,
                             group_partner_invoice_id)
            elif group_method == 'nothing':
                group_key = self.id
        else:
            group_key = self.id

        return group_key

    def _get_sale_order_ref(self):
        sale_order = False
        if self.move_lines and self.move_lines[0] and self.move_lines[0].sale_line_id:
            sale_order = self.move_lines[0].sale_line_id.order_id

        return sale_order


class StockPickingPackagePreparation(models.Model):
    _inherit = "stock.picking.package.preparation"

    @api.multi
    def get_td_group_key(self):
        """
        if group into context is False group_key is the TD id
        which makes one invoice per td
        """
        if self._context.get('group', True):
            group_key = super().get_td_group_key()
        else:
            group_key = self.id
        # end if

        return group_key

    @api.multi
    def _prepare_invoice(self):
        """
        override j
        """
        self.ensure_one()

        res = super()._prepare_invoice()

        journal_id = self._context.get('invoice_journal_id', res['journal_id'])
        if journal_id:
            res.update({
                'journal_id': journal_id,
            })

        return res

    @api.multi
    def create_td_grouped_invoices(self):
        """
        Create the invoices, grouped by `group_key` (see `get_td_group_key`).
        :return: (
            dictionary group_key -> invoice record-set,
            dictionary invoice -> TD record-set,
            )
        """
        grouped_invoices, references = super().create_td_grouped_invoices()
        if grouped_invoices:
            journal_id = self._context.get('invoice_journal_id', False)
            if journal_id:
                for invoice in list(grouped_invoices.values()):
                    invoice.write({
                        'journal_id': journal_id
                    })
        return grouped_invoices, references

    @api.multi
    def action_invoice_create_wcontext(self, cntx=None):
        if cntx:
            self = self.with_context(cntx)
        self.action_invoice_create()


