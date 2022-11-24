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
from odoo import models, fields, api
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp

from odoo.fields import first
from odoo.tools import float_is_zero
from odoo.tools.misc import formatLang, format_date


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    credit_note = fields.Many2one(
        'account.invoice',
        string='Credit note',
        readonly=True
    )

    returned_by = fields.Boolean(
        string='Returned by customer',
        default=False,
    )

    @api.multi
    def action_invoice_refund(self):
        #
        grouped_invoices, references = self.create_td_grouped_invoices()
        if not grouped_invoices:
            raise UserError(_('There is no invoiceable line.'))

        for invoice in list(grouped_invoices.values()):
            if not invoice.name:
                invoice.update({
                    'name': invoice.origin,
                })

        return [inv.id for inv in list(grouped_invoices.values())]

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

            for line in sp.move_ids_without_package:
                if line.product_uom_qty > 0:
                    line.invoice_line_create(invoice, line.product_uom_qty)

        return grouped_invoices, references

    @api.multi
    def _prepare_invoice(self):

        self.ensure_one()
        res = {
            'type': 'out_refund',
            'company_id': self.company_id.id
        }
        journal_id = self._context.get('invoice_journal_id', False)

        if not journal_id:
            raise UserError(
                'Registro per movimenti per note di credito non impostato.'
            )
        journal = self.env['account.journal'].browse(journal_id)

        invoice_partner_id = self.partner_id.id
        invoice_partner = self.partner_id

        invoice_description = '' # self._prepare_invoice_description()
        currency_id = journal.currency_id.id or journal.company_id.currency_id.id

        payment_term_id = self.partner_id.property_payment_term_id.id

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

    @api.multi
    def get_td_group_key(self):
        """
        Get the grouping key for current SP.
        """
        self.ensure_one()
        if self._context.get('group', True):
            group_key = super().get_td_group_key()
        else:
            group_key = self.id

        return group_key


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
        res.update({
            'journal_id': journal_id,
        })

        return res

