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
import logging
from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class WizardInvoiceFromDdt(models.TransientModel):
    _name = 'wizard.invoice.from.ddt'
    _description = 'Fatture da DDT'

    date_from = fields.Date(
        string='Date from',
        required=True,
    )

    date_to = fields.Date(
        string='Date to',
        required=True,
    )

    date_invoice = fields.Date(
        string='Date invoice',
        required=True,
    )

    journal_id = fields.Many2one(
        'account.journal',
        string='Invoice journal',
        domain=[('type', '=', 'sale')],
        required=True,
    )

    journal_id_refund = fields.Many2one(
        'account.journal',
        string='Refund journal',
        domain=[('type', '=', 'sale')],
        required=True,
    )

    group_by_partner = fields.Boolean(
        string='Group by Partner',
        default=True,
    )

    @api.multi
    def create_invoice(self):
        _logger.info('Creating invoices......')

        if self.date_from > self.date_to:
            raise UserError('Attenzione!\nVerificare l\'intervallo delle date del periodo.')

        group = self.group_by_partner

        # elenco ddt del periodo per fatture di vendita
        return_ids = list()
        domain = list()
        domain.append(('to_be_invoiced', '=', True))
        domain.append(('invoice_id', '=', False))
        domain.append(('state', '=', 'done'))
        if self.date_from:
            domain.append(('date', '>=', self.date_from))
        if self.date_to:
            domain.append(('date', '<=', self.date_to))

        ddt = self.env['stock.picking.package.preparation'].search(domain)
        if ddt:
            cntx = {'invoice_date': self.date_invoice, 'invoice_journal_id': self.journal_id.id}
            if group is False:
                cntx.update({'group': False})
            return_ids = ddt.with_context(cntx).action_invoice_create()
            # print(return_ids)

        # elenco movimenti per note di credito
        sp_domain = list()
        sp_domain.append(('returned_by', '=', True))
        sp_domain.append(('state', '=', 'done'))
        sp_domain.append(('credit_note', '=', False))
        if self.date_from:
            sp_domain.append(('date', '>=', self.date_from))
        if self.date_to:
            sp_domain.append(('date', '<=', self.date_to))

        sp_in = self.env['stock.picking'].search(sp_domain)
        if sp_in:
            cntx = {'invoice_date': self.date_invoice, 'invoice_journal_id': self.journal_id_refund.id}
            if group is False:
                cntx.update({'group': False})
            return_ids += sp_in.with_context(cntx).action_invoice_refund()
            
        return {'type': 'ir.actions.act_window_close'}
