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
import time
import datetime
import multiprocessing
import threading
from odoo import models, fields, api, registry
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class WaitCreditNoteProcess(threading.Thread):
    def __init__(self, env, ddt_ids, wizard_domain, processes):
        threading.Thread.__init__(self)
        self.ddt_ids = ddt_ids
        self.wizard_domain = wizard_domain
        self.data_env = env
        self.number_of_processes = processes
        with api.Environment.manage():
            with registry(env[0]).cursor() as new_cr:
                self.new_env = api.Environment(new_cr, env[1], env[2])
        self.cr = self.new_env.cr

    def run(self):
        _logger.info(f'WaitCreditNoteProcess running..{self.wizard_domain}')

        with api.Environment.manage():
            with registry(self.data_env[0]).cursor() as new_cr:
                current_env = api.Environment(new_cr, self.data_env[1], self.data_env[2])
                cursor = current_env.cr

                def _chunkIt(seq, size):
                    newseq = []
                    splitsize = 1.0 / size * len(seq)
                    for line in range(size):
                        newseq.append(seq[int(round(line * splitsize)):int(round((line + 1) * splitsize))])
                    return newseq

                ddt_ids = self.ddt_ids
                domain = self.wizard_domain + [('id', 'in', ddt_ids)]
                while ddt_ids:

                    try:
                        number_of_processes = self.number_of_processes
                        if number_of_processes <= 0:
                            number_of_processes = multiprocessing.cpu_count() // 2
                        cpus_available = number_of_processes or 1
                        i = 0
                        threads = []
                        stock_model = current_env['stock.picking']
                        res = stock_model.read_group(domain,
                                                     fields=['main_partner', 'id'],
                                                     groupby=['main_partner'],
                                                     orderby='main_partner',
                                                     lazy=False)

                        with multiprocessing.Manager() as manager:
                            invoice_ids = manager.list()
                            for split in _chunkIt(res, cpus_available):
                                if split:
                                    thread = CreateCreditNoteProcess(self.data_env, split, i, invoice_ids)
                                    thread.daemon = True
                                    thread.start()
                                    threads.append(thread)
                                    i += 1
                            # wait for invoice created
                            for job in threads:
                                job.join()

                    except Exception as e:
                        # Annulla le modifiche fatte
                        _logger.error(u'Error: {error}'.format(error=e))
                        cursor.rollback()
                        raise
                    finally:
                        ddt_ids = list()


class CreateCreditNoteProcess(multiprocessing.Process):

    def __init__(self, env, partner_list, name_process, invoice_ids):
        # Inizializzazione superclasse
        multiprocessing.Process.__init__(self)
        self.partner_list = partner_list
        self.name_process = name_process
        self.invoice_ids = invoice_ids
        self.data_env = env
        with api.Environment.manage():
            with registry(env[0]).cursor() as new_cr:
                self.new_env = api.Environment(new_cr, env[1], env[2])
        self.cr = self.new_env.cr

    def run(self):
        _logger.info(f'CreateCreditNoteProcess running..{self.name_process}')

        with api.Environment.manage():
            with registry(self.data_env[0]).cursor() as new_cr:
                current_env = api.Environment(new_cr, self.data_env[1], self.data_env[2])
                cursor = current_env.cr
                try:
                    cntx = self.data_env[2]
                    wiz_id = cntx['wizard_id']
                    wizard = current_env['wizard.credit.note.from.picking'].browse(cntx['wizard_id'])
                    for partner_group in self.partner_list:
                        domain = wizard.domain_x_credit_note()
                        main_partner_id = partner_group['main_partner'][0]
                        domain.append(('main_partner', '=', main_partner_id))
                        stock_picking_to_invoice_ids = current_env['stock.picking'].sudo().search(domain)
                        #
                        # stock_picking_to_invoice_ids = current_env['stock.picking'].sudo().search(
                        #     partner_group.get('__domain'))
                        pterm = {}
                        for sp in stock_picking_to_invoice_ids:
                            order = sp.move_lines and sp.move_lines[0].sale_line_id and sp.move_lines[0].sale_line_id.order_id or False
                            if order:
                                pti_id = order.payment_term_id and order.payment_term_id.id or False
                            else:
                                if sp.partner_id.property_payment_term_id:
                                    pti_id = sp.partner_id.property_payment_term_id.id
                                else:
                                    pti_id = False
                            if pti_id:
                                if pti_id not in pterm:
                                    pterm[pti_id] = current_env['stock.picking']
                                    pterm[pti_id] |= sp
                                else:
                                    pterm[pti_id] |= sp
                            else:
                                if 'ZZZZ' not in pterm:
                                    pterm['ZZZZ'] = current_env['stock.picking']
                                pterm['ZZZZ'] |= sp

                        try:
                            for key, value in pterm.items():
                                create_invoice_res = value.with_context(cntx).action_invoice_refund()
                            # _logger.info(u'{id}: Finish create invoice'.format(id=self.name_process))
                        except Exception as e:
                            # Annulla le modifiche fatte
                            _logger.error(u'{id}: Error: {error}'.format(id=self.name_process, error=e))
                            _logger.error(u'Error: {error}'.format(error=pterm.keys()))
                            cursor.rollback()
                        finally:
                            cursor.commit()
                    cursor.commit()
                except Exception as e:
                    # Annulla le modifiche fatte
                    _logger.error(u'{id}: Error: {error}'.format(id=self.name_process, error=e))
                    cursor.rollback()
                _logger.info(u'{id}: Finish Process'.format(id=self.name_process))


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

    # finished_invoices = fields.Boolean(
    #     string='',
    #     default=False,
    # )
    #
    # finished_invoices_message = fields.Text(
    #     string='',
    #     default='La generazione delle fatture è terminata con successo.',
    # )

    @api.multi
    def create_credit_note(self):
        if self.date_from > self.date_to:
            raise UserError('Attenzione!\nVerificare l\'intervallo delle date del periodo.')

        start_time = datetime.datetime.now()
        # elenco movimenti per note di credito
        _logger.info('Create credit notes ......')

        refund_ids = self.create_from_stock_picking()

        end_time = datetime.datetime.now()
        duration_seconds = (end_time - start_time).seconds
        duration = '{min}m {sec}sec'.format(min=duration_seconds / 60,
                                            sec=duration_seconds - duration_seconds / 60 * 60)
        _logger.info(u'Note di credito Execution time in: {0}'.format(duration))

        # return {'type': 'ir.actions.act_window_close'}
        return {
            "type": "ir.action.do_nothing",
        }

    def create_from_stock_picking(self):
        sp_domain = self.domain_x_credit_note()
        dbname = self.env.cr.dbname
        uid = self.env.uid
        processes = self.env.user.company_id.sudo().number_of_processes
        context = dict(self._context)
        context.update({'invoice_date': self.date_invoice,
                        'wizard_id': self.id,
                        'refund_journal_id': self.journal_id_refund.id})
        if self.group_by_partner is False:
            context.update({'group': False})

        env = (dbname, uid, context)
        pickings = self.env['stock.picking'].search(sp_domain)
        final_process = WaitCreditNoteProcess(env, pickings.ids, sp_domain, processes)
        final_process.start()

        return sp_domain

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

