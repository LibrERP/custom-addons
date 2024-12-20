# © 2020 Andrei Levin - Didotech srl (www.didotech.com)
# © 2024-* Andrei Levin - Codebeex srl (www.codebeex.com)


E_INVOICE_STATE = [
    ('ready', 'Ready to Send'),
    ('sent', 'Sent'),
    ('error', 'Error'),
    ('NS', 'Notifica di Scarto'),
    ('MC', 'Notifica di Mancata Consegna'),
    ('RC', 'Ricevuta di Consegna'),
    ('EC_ACCETTAZIONE', 'Notifica di Esito Committente: ACCETTATA'),
    ('EC_RIFIUTO', 'Notifica di Esito Committente: RIFIUTATA'),
    ('SE', 'Notifica di Scarto Esito Committente'),
    ('NE', 'Notifica di Esito'),
    ('NE_ACCETTAZIONE', 'Notifica di Esito: ACCETTATA'),
    ('NE_RIFIUTO', 'Notifica di Esito: RIFIUTATA'),
    ('DT', 'Notifica di decorrenza di Decorrenza Termini'),
    ('AT', 'Attestazione di avvenuta trasmissione con impossibilità di recapito'),
    ('MT', 'Metadati'),
    ('ED', 'ED'),
    ('EF', 'EF'),
    ('EL', 'EL'),
    ('NA', 'NA'),
    ('NONE', 'Nessuna notifica')
]

E_INVOICE_STATE_TRANSLATION = {
    'NS': 'sender_error',  # 2A. Notifica di Scarto
    'MC': 'recipient_error',  # 3A. Mancata consegna
    'RC': 'validated',  # 3B. Ricevuta di Consegna
    'NE': 'sent',  # 4A. Notifica Esito per PA
    'NE_ACCETTAZIONE': 'accepted',
    'NE_RIFIUTO': 'rejected',
    'DT': 'validated',  # 5. Decorrenza Termini per PA
    'AT': 'accepted'  # 6. Avvenuta Trasmissione per PA
}


class ActiveInvoice:
    def __init__(self, config, dry_run=False):
        self.useralias = config.sdi_username
        self.password = bytearray(config.sdi_password, 'utf-8')
        self.node = config.sdi_node
        self.my_node = config.node

    def upload_data(self, document_name, data, dry_run=False):
        pass

    def send_invoice(self, email=False):
        """
        Invio fattura precaricata a SdI
        :param email: Lista indirizzi e-Mail a cui recapitare la fattura elettronica
        :return: esito dell'invio lista di identificativo sdi e data ora invio
                 oppure un errore
        """
        pass

    def get_log_invoice(self, sdi_id=None, sdi_filename=None, from_date=None, to_date=None):
        pass

    def get_invoice(self, sdi_id, estrazioneP7M=True):
        """
        Recupera il file XML della fattura precedentemente inviata
        :param idsdi: identificativo assegnato da SdI
        :param estrazioneP7M:
        :return: fatturaPA XML codificata in Base 64
        """
        pass

    def get_sending_result(self, sdi_id):
        """
        Esito invio FatturaPA. Interroga 2C per conoscere l'esito dell'invio fattura
        :param idsdi: identificativo assegnato da SdI
        :return: codice esito SdI/2C
        """
        pass

    def send_email(self, sdi_id, email):
        pass

    def upload_invoice(self, invoice_out, doucment_host, config):
        pass

    def _hook_after_sent(self, fatturapa_attachment_out):
        return True

    def update_status(self):
        pass


class PassiveInvoice:
    pass
