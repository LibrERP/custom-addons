# -*- coding: utf-8 -*-
# © 2013-2017 Didotech srl (www.didotech.com)
# © 2013-2017 Andrei Levin (andrei.levin at didotech.com)

from datetime import datetime
import math
import threading
import re
import logging
from odoo import api, _
from odoo.addons.core_extended.file_manipulation import import_sheet
from odoo.addons.data_migration import settings

_logger = logging.getLogger(__name__)
DEBUG = settings.DEBUG
# DEBUG = True
if DEBUG:
    import pdb
    _logger.setLevel(logging.DEBUG)
else:
    _logger.setLevel(logging.INFO)


class BaseImport(object):
    def __init__(self, env, import_record_id=False, import_model=False):
        self.error = []
        self.warning = []
        self.first_row = True

        # Contatori dei nuovi prodotti inseriti e dei prodotti aggiornati,
        # vengono utilizzati per compilare il rapporto alla terminazione
        # del processo di import
        self.new = 0
        self.updated = 0
        self.problems = 0
        self.progress_indicator = 0
        self.env = env
        if import_record_id:
            self.import_record = self.env[import_model].browse(import_record_id)
            self.file_name = self.import_record.file_name.split('\\')[-1]
        else:
            self.import_record = False

        self.start_time = datetime.now()

    def import_data(self):
        return import_sheet(self.file_name, self.import_record.content_text, ';')

    def run(self):
        # Recupera i record
        table, self.number_of_lines = self.import_data()
        self.processed_lines = 0
        if DEBUG:
            self.process(table)

            # Genera il report sull'importazione
            self.notify_import_result(self.message_title, 'Importazione completata', record=self.import_record)
        else:
            # Elaborazione del listino prezzi
            try:
                self.process(table)

                # Genera il report sull'importazione
                self.notify_import_result(self.message_title, 'Importazione completata', record=self.import_record)
            except Exception as e:
                # Annulla le modifiche fatte
                self.env.cr.rollback()
                self.env.cr.commit()

                title = "Import failed"
                message = "Errore alla linea %s" % self.processed_lines + "\nDettaglio:\n\n" + str(e)
                _logger.debug(message)

                if DEBUG:
                    ### Debug
                    pdb.set_trace()

                self.notify_import_result(title, message, error=True)
        return True

    def process(self, table):
        notify_progress_step = int(self.number_of_lines / 100) + 1     # NB: divisione tra interi da sempre un numero intero!
                                                                # NB: il + 1 alla fine serve ad evitare divisioni per zero

        # Use counter of processed lines
        # If this line generate an error we will know the right Line Number
        # for self.processed_lines, row_list in enumerate(table, start=1):
        for row_list in table:
            self.processed_lines += 1
            if not self.import_row(row_list):
                self.problems += 1

            if (self.processed_lines % notify_progress_step) == 0:
                self.env.cr.commit()
                completed_quota = float(self.processed_lines) / float(self.number_of_lines)
                completed_percentage = math.trunc(completed_quota * 100)
                self.update_progress_indicator(completed_percentage)

        if hasattr(self, 'post_import'):
            self.post_import()

        self.update_progress_indicator(100)
        return True

    def update_progress_indicator(self, progress):
        self.import_record.progress_indicator = progress
        _logger.info('>>> Import status: {0}% ({1} lines processed)'.format(self.import_record.progress_indicator, self.processed_lines))

    @classmethod
    def to_string(cls, value):
        if value:
            if isinstance(value, str) and value.lower() == 'null':
                return False

            number = re.compile(r'^(?!0[0-9])[0-9.,]+(?<![.,])$')
            number_with_thousands_separator_italian = re.compile(r'[0-9]{1,3}(\.+[0-9]{3})+,[0-9]{2}$')
            number_with_thousands_separator = re.compile(r'[0-9]{1,3}(,+[0-9]{3})+\.[0-9]{2}$')
            if isinstance(value, str):
                if number.match(value):
                    if ',' in value or '.' in value:
                        if number_with_thousands_separator_italian.match(value):
                            value = value.replace('.', '')
                        elif number_with_thousands_separator.match(value):
                            value = value.replace(',', '')
                        else:
                            if value[0] == '+':
                                return value
                            elif value.count('.') > 1:
                                # not a number
                                return value

                        value = value.replace(',', '.')
                        value = float(value)
                    else:
                        value = int(value)
                    return value
                else:
                    return value.strip()
            else:
                if value:
                    if int(value) == value:
                        # Trim .0
                        return str(int(value), 'utf-8')
                    else:
                        return str(value, 'utf-8')
                else:
                    return False
        else:
            return False
    
    def notify_import_result(self, title, body='', error=False, record=False):
        EOL = '\n<br/>'
        end_time = datetime.now()
        duration_seconds = (end_time - self.start_time).seconds
        duration = '{min}m {sec}sec'.format(min=duration_seconds / 60, sec=duration_seconds - duration_seconds / 60 * 60)
        if not error:
            body += EOL + EOL
            body += u"File '{0}' {1}{1}".format(self.file_name, EOL)
            body += _(u"Importate righe: {self.new}{eol}Righe non importate: {self.problems}{eol}").format(self=self, eol=EOL)
            body += _(u"Righe aggiornate: {0}{1}{1}").format(self.updated, EOL)
            # body += _(u"Righe ignorate: {0}{1}").format(self.ignored, EOL)
            body += _('Inizio: {0}{1}').format(self.start_time.strftime('%Y-%m-%d %H:%M:%S'), EOL)
            body += _('Fine: {0}{1}').format(end_time.strftime('%Y-%m-%d %H:%M:%S'), EOL)
            body += _('Importazione eseguita in: {0}{1}{1}').format(duration, EOL)

            if self.error:
                body += u'{0}{0}<strong>Errors:</strong>{0}'.format(EOL) + EOL.join(self.error)
                
            if self.warning:
                body += u'{0}{0}<strong>Warnings:</strong>{0}'.format(EOL) + EOL.join(self.warning)
        
        mail = self.env['mail.mail'].create({
            'subject': title,
            'email_to': self.env.user.company_id.email,
            'body_html': body,
            'model': self.import_record._name
        })

        if record:
            # add file to attachment of email for future use
            self.env['mail.mail'].write({
                'attachment_ids': [(0, 0, {
                    'res_model': 'mail.mail',
                    'name': record.file_name.split('\\')[-1],
                    'datas_fname': record.file_name,
                    'datas': record.content_base64,
                    'res_id': mail.id
                })]
            })

        _logger.debug(body)
        
        # Salva il messaggio nel database
        self.env.cr.commit()
        # chiudi la connessione
        # self.env.cr.close()
        return True


class ThreadingImport(threading.Thread, BaseImport):
    """
    Actually this class give environment error. Needs investigation
    self.env['product.category'].browse(6).name = 600
    """
    def __init__(self, old_env, import_record_id, import_model):
        threading.Thread.__init__(self)

        # Necessario creare un nuovo cursor and Environment per il thread,
        # quello fornito dal metodo chiamante viene chiuso
        # alla fine del metodo e diventa inutilizzabile
        # all'interno del thread.
        # new_cr = pooler.get_db(old_env.cr.dbname).cursor()
        with api.Environment.manage(), self.pool.cursor() as new_cr:
            self.env = api.Environment(new_cr, old_env.uid, old_env.context)

        # Inizializzazione superclasse
        BaseImport.__init__(self, self.env, import_record_id, import_model=import_model)

    def run(self):
        BaseImport.run(self)
