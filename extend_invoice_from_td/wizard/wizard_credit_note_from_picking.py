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


class WizardCreditNoteFromPicking(models.TransientModel):
    _name = 'wizard.credit.note.from.picking'
    _description = 'Note di credito da resi'

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
    def create_credit_note(self):
        if self.date_from > self.date_to:
            raise UserError('Attenzione!\nVerificare l\'intervallo delle date del periodo.')

        c_notes_creation_context = self.get_custom_context()

        #                         res = stock_model.read_group(domain,
        #                                                      fields=['main_partner', 'id'],
        #                                                      groupby=['main_partner'],
        #                                                      orderby='main_partner',
        #                                                      lazy=False)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Raggruppamento Picking
        picking_groups_list = self.env['stock.picking'].read_group(
            domain=self.domain_x_credit_note(),
            fields=['main_partner', 'ids:array_agg(id)'],
            groupby=['main_partner'],
            orderby='main_partner',
            lazy=False,
        )

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Fatturazione di ciascun gruppo di picking
        total_cnotes_create_begin = time.time()

        for picking_group in picking_groups_list:

            domain = self.domain_x_credit_note()
            main_partner_id = picking_group['main_partner'][0]
            domain.append(('main_partner', '=', main_partner_id))
            stock_picking_to_invoice_ids = self.env['stock.picking'].sudo().search(domain)
            pterm = {}
            for sp in stock_picking_to_invoice_ids:
                order = sp.move_lines and sp.move_lines[0].sale_line_id and sp.move_lines[
                    0].sale_line_id.order_id or False
                if order:
                    pti_id = order.payment_term_id and order.payment_term_id.id or False
                else:
                    if sp.partner_id.property_payment_term_id:
                        pti_id = sp.partner_id.property_payment_term_id.id
                    else:
                        pti_id = False
                if pti_id:
                    if pti_id not in pterm:
                        pterm[pti_id] = self.env['stock.picking']
                        pterm[pti_id] |= sp
                    else:
                        pterm[pti_id] |= sp
                else:
                    if 'ZZZZ' not in pterm:
                        pterm['ZZZZ'] = self.env['stock.picking']
                    pterm['ZZZZ'] |= sp

            # picking_recordset = self.env['stock.picking'].browse(picking_group['ids'])

            # Creazione fattura e conferma transazione DB

            group_cnotes_create_begin = time.time()

            for key, picking_recordset in pterm.items():
                picking_recordset.with_delay().action_invoice_refund_wcontext(
                    c_notes_creation_context)  # Fatturazione con job queue e processi multipli

                _logger.info(
                    '\n\n'
                    '====>> ====>> ====>> ====>> BEGIN'
                    f'\n\n[Invoice Refund from Picking] Start invoicing for {len(picking_recordset)} Picking '
                )

                group_cnotes_create_time = time.time() - group_cnotes_create_begin

                _logger.info(
                    f'[Invoice Refund from Pickings] Completed invoicing for {len(picking_recordset)} Pickings in {group_cnotes_create_time}s'
                    '\n\n'
                    '<<==== <<==== <<==== <<==== END'
                    '\n\n'
                )
        # end for

        total_cnotes_create_time = time.time() - total_cnotes_create_begin
        _logger.info(
            f'[Credit Notes from Pickings] Completed invoicing for {len(picking_groups_list)} groups in {total_cnotes_create_time}s'
            f'\n\n\n\n'
        )
        # end for
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # end create_credit_note

    def domain_x_credit_note(self, other_conditions=[]):
        sp_domain = list()
        sp_domain.append(('returned_by', '=', True))
        sp_domain.append(('state', '=', 'done'))
        sp_domain.append(('credit_note', '=', False))
        if self.date_from:
            sp_domain.append(('date_done', '>=', self.date_from))
        if self.date_to:
            sp_domain.append(('date_done', '<=', self.date_to))
        if other_conditions:
            for tpl in other_conditions:
                sp_domain.append(tpl)

        return sp_domain

    def get_custom_context(self):
        custom_context = dict(self._context)

        custom_context.update({
            'invoice_date': self.date_invoice,
            'wizard_id': self.id,
            'refund_journal_id': self.journal_id_refund.id,
        })

        if self.group_by_partner is False:
            custom_context.update({'group': False})
        # end if

        return custom_context
    # end get_custom_context
