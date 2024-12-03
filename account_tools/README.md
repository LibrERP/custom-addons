Per personalizzare il modulo di Chart of Account (Piano dei Conti) è necessario
ricreare o modificare i seguenti file:

    - account.account-it.csv - file che contiene proprio il Piano dei Conti, deve essere rinominato. 
        Per esempio per l'azienda t2: account.account-it_t2.csv
    - account.fiscal.position-it.csv - Deve essere solo rinominato in account.fiscal.position-it_t2.csv
    - account.tax.group-it.csv - I valori dei conti devono essere modificati per corrispondere al Piano dei Conti.
        File deve essere rinominato in account.tax.group-it_t2.csv
    - account.tax-it.csv - I valori dei conti devono essere modificati per corrispondere al Piano dei Conti.
        File deve essere rinominato in account.tax-it_t2.csv
    - account.group-it_t2.xml - File contiene i gruppi e deve essere creato da zero. 
        Durante l'installazione è necessario impostare noupdate="0". 
        Dopo aver verificato che i gruppi sono installati rimettere noupdate="1"
    - account_report.py - Modificare il nome del modulo nel path. In caso di Urmet l10n_it diventa l10n_it_t2_coa
    - template_it.py - Sostituire i conti con i conti di Urmet
    - __manifest__.py - Addiungere il path al account.group-it_t2.xml

Per produrre i file di PdC e Gruppi usare lo script create_account_files.py:

    create_account_files.py -F account.account-t2.csv
