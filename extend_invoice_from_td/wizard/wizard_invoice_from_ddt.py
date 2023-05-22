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
import collections
import logging
import time

from odoo import models, fields, api, registry
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


OdooEnv = collections.namedtuple('OdooEnv', ['dbname', 'uid', 'context'])


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

    group_by_partner = fields.Boolean(
        string='Group by Partner',
        default=True,
    )

    @api.multi
    def create_invoice(self):

        if self.date_from > self.date_to:
            raise UserError('Attenzione!\nVerificare l\'intervallo delle date del periodo.')
        # end if

        invoice_creation_context = self.get_custom_context()

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Raggruppamento DDT
        ddt_groups_list = self.env['stock.picking.package.preparation'].read_group(
            domain=self.get_domain_for_ddt(),
            fields=['partner_id', 'payment_term_id', 'ids:array_agg(id)'],
            groupby=['partner_id', 'payment_term_id'],
            orderby='partner_id, payment_term_id',
            lazy=False,
        )

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Fatturazione di ciascun gruppo di DDT
        total_inv_create_begin = time.time()
        for ddt_group in ddt_groups_list:

            ddts_recordset = self.env['stock.picking.package.preparation'].browse(ddt_group['ids'])

            # Creazione fattura e conferma transazione DB
            _logger.info(
                '\n\n'
                '====>> ====>> ====>> ====>> BEGIN'
                f'\n\n[Invoice from DDT] Start invoicing for {len(ddts_recordset)} DDTs'
            )
            group_inv_create_begin = time.time()

            # ddts_recordset.with_context(invoice_creation_context).with_delay().action_invoice_create()  # Fatturazione con job queue e processi multipli
            ddts_recordset.with_delay().action_invoice_create_wcontext(invoice_creation_context)  # Fatturazione con job queue e processi multipli
            # ddts_recordset.with_context(invoice_creation_context).action_invoice_create()  # Fatturazione con processo singolo
            group_inv_create_time = time.time() - group_inv_create_begin
            _logger.info(
                f'[Invoice from DDT] Completed invoicing for {len(ddts_recordset)} DDTs in {group_inv_create_time}s'
                '\n\n'
                '<<==== <<==== <<==== <<==== END'
                '\n\n'
            )
        # end for

        total_inv_create_time = time.time() - total_inv_create_begin
        _logger.info(
            f'[Invoice from DDT] Completed invoicing for {len(ddt_groups_list)} groups in {total_inv_create_time}s'
            f'\n\n\n\n'
        )
        # end for
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # end create_from_ddt

    def get_custom_context(self):
        custom_context = dict(self._context)

        custom_context.update({
            'invoice_date': self.date_invoice,
            'wizard_id': self.id,
            'invoice_journal_id': self.journal_id.id,
        })

        if self.group_by_partner is False:
            custom_context.update({'group': False})
        # end if

        return custom_context
    # end get_custom_context

    def get_domain_for_ddt(self, other_conditions=None):

        domain = [
            ('to_be_invoiced', '=', True),
            ('invoice_id', '=', False),
            ('state', '=', 'done'),
        ]

        if self.date_from:
            domain.append(('date', '>=', self.date_from))

        if self.date_to:
            domain.append(('date', '<=', self.date_to))

        if other_conditions:
            domain += other_conditions

        return domain
    # end get_domain_for_ddt

# WizardInvoiceFromDdt
