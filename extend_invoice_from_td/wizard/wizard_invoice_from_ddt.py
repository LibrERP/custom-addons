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


class WaitInvoiceProcess(threading.Thread):
    def __init__(self, env, ddt_ids, wizard_domain):
        threading.Thread.__init__(self)
        self.ddt_ids = ddt_ids
        self.wizard_domain = wizard_domain
        self.data_env = env
        with api.Environment.manage():
            with registry(env[0]).cursor() as new_cr:
                self.new_env = api.Environment(new_cr, env[1], env[2])
        self.cr = self.new_env.cr

    def run(self):
        _logger.info(f'WaitInvoiceProcess running..{self.wizard_domain}')

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
                        cpus_available = multiprocessing.cpu_count() - 1 or 1
                        i = 0
                        threads = []
                        stock_model = current_env['stock.picking.package.preparation']
                        res = stock_model.read_group(domain,
                                                     fields=['partner_id', 'id'],
                                                     groupby=['partner_id'],
                                                     orderby='partner_id',
                                                     lazy=False)

                        with multiprocessing.Manager() as manager:
                            invoice_ids = manager.list()
                            for split in _chunkIt(res, cpus_available):
                                if split:
                                    thread = CreateInvoiceProcess(self.data_env, split, i, invoice_ids)
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


class CreateInvoiceProcess(multiprocessing.Process):

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
        _logger.info(f'CreateInvoiceProcess running..{self.name_process}')

        with api.Environment.manage():
            with registry(self.data_env[0]).cursor() as new_cr:
                current_env = api.Environment(new_cr, self.data_env[1], self.data_env[2])
                cursor = current_env.cr
                try:
                    cntx = self.data_env[2]
                    for partner_group in self.partner_list:
                        stock_picking_to_invoice_ids = current_env['stock.picking.package.preparation'].search(
                            partner_group.get('__domain'))
                        try:

                            create_invoice_res = stock_picking_to_invoice_ids.with_context(cntx).action_invoice_create()
                            # _logger.info(u'{id}: Finish create invoice'.format(id=self.name_process))
                        except Exception as e:
                            # Annulla le modifiche fatte
                            _logger.error(u'{id}: Error: {error}'.format(id=self.name_process, error=e))
                            cursor.rollback()
                        finally:
                            cursor.commit()
                    cursor.commit()
                except Exception as e:
                    # Annulla le modifiche fatte
                    _logger.error(u'{id}: Error: {error}'.format(id=self.name_process, error=e))
                    cursor.rollback()
                _logger.info(u'{id}: Finish Process'.format(id=self.name_process))


class WaitCreditNoteProcess(threading.Thread):
    def __init__(self, env, ddt_ids, wizard_domain):
        threading.Thread.__init__(self)
        self.ddt_ids = ddt_ids
        self.wizard_domain = wizard_domain
        self.data_env = env
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
                        cpus_available = multiprocessing.cpu_count() - 1 or 1
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
                    for partner_group in self.partner_list:
                        stock_picking_to_invoice_ids = current_env['stock.picking'].search(
                            partner_group.get('__domain'))
                        try:

                            create_invoice_res = stock_picking_to_invoice_ids.with_context(cntx).action_invoice_refund()
                            # _logger.info(u'{id}: Finish create invoice'.format(id=self.name_process))
                        except Exception as e:
                            # Annulla le modifiche fatte
                            _logger.error(u'{id}: Error: {error}'.format(id=self.name_process, error=e))
                            cursor.rollback()
                        finally:
                            cursor.commit()
                    cursor.commit()
                except Exception as e:
                    # Annulla le modifiche fatte
                    _logger.error(u'{id}: Error: {error}'.format(id=self.name_process, error=e))
                    cursor.rollback()
                _logger.info(u'{id}: Finish Process'.format(id=self.name_process))


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
    def create_invoice(self):
        if self.date_from > self.date_to:
            raise UserError('Attenzione!\nVerificare l\'intervallo delle date del periodo.')

        _logger.info('Creating invoices......')
        start_time = datetime.datetime.now()

        _logger.info('Create invoices ......')

        invoice_ids = self.create_from_ddt()

        _logger.info('Invoices created')
        end_time = datetime.datetime.now()
        duration_seconds = (end_time - start_time).seconds
        duration = '{min}m {sec}sec'.format(min=duration_seconds / 60,
                                            sec=duration_seconds - duration_seconds / 60 * 60)
        _logger.info(u'Fatture Execution time in: {0}'.format(duration))

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

    def create_from_ddt(self):
        domain = self.domain_x_invoice()
        dbname = self.env.cr.dbname
        uid = self.env.uid
        context = dict(self._context)
        context.update({'invoice_date': self.date_invoice, 'invoice_journal_id': self.journal_id.id})
        if self.group_by_partner is False:
            context.update({'group': False})

        env = (dbname, uid, context)
        ddts = self.env['stock.picking.package.preparation'].search(domain)
        final_process = WaitInvoiceProcess(env, ddts.ids, domain)
        final_process.start()
        return domain

    def create_from_stock_picking(self):
        sp_domain = self.domain_x_credit_note()
        dbname = self.env.cr.dbname
        uid = self.env.uid
        context = dict(self._context)
        context.update({'invoice_date': self.date_invoice,
                        'refund_journal_id': self.journal_id_refund.id})
        if self.group_by_partner is False:
            context.update({'group': False})

        env = (dbname, uid, context)
        pickings = self.env['stock.picking'].search(sp_domain)
        final_process = WaitCreditNoteProcess(env, pickings.ids, sp_domain)
        final_process.start()

        return sp_domain

    def domain_x_invoice(self, other_conditions=[]):
        domain = list()
        domain.append(('to_be_invoiced', '=', True))
        domain.append(('invoice_id', '=', False))
        domain.append(('state', '=', 'done'))
        if self.date_from:
            domain.append(('date', '>=', self.date_from))
        if self.date_to:
            domain.append(('date', '<=', self.date_to))
        if other_conditions:
            for tpl in other_conditions:
                domain.append(tpl)

        return domain

    def domain_x_credit_note(self, other_conditions=[]):
        sp_domain = list()
        sp_domain.append(('returned_by', '=', True))
        sp_domain.append(('state', '=', 'done'))
        sp_domain.append(('credit_note', '=', False))
        if self.date_from:
            sp_domain.append(('date', '>=', self.date_from))
        if self.date_to:
            sp_domain.append(('date', '<=', self.date_to))
        if other_conditions:
            for tpl in other_conditions:
                sp_domain.append(tpl)

        return sp_domain

