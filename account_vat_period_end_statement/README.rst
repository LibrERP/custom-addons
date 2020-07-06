
========================================
|icon| ITA - Liquidazione IVA 12.0.1.3.0
========================================


**Versamento Iva periodica (mensile o trimestrale)**

.. |icon| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy/12.0/account_vat_period_end_statement/static/description/icon.png

|Maturity| |Build Status| |Codecov Status| |license gpl| |Try Me|


.. contents::


Overview / Panoramica
=====================

|en| This module evaluates VAT to pay (or on credit).

Previous debit or credit amount is read from previous VAT statement, according
to its payments status.


|

|it| Versamento Iva periodica

::

    Cosa è:

Modulo per calcolare l'importo IVA da pagare (o a credito) sia per i contribuenti
mensili che trimestrali.
L'importo del versamento deve essere dichiarato per via telemativa con il modello F24 (non gestito da questo modulo).

L'IVA è calcolata dalle registrazioni contabili inerenti i registri IVA.
Inoltre viene sottratto l’eventuale credito d’imposta del periodo precedente (o l’eventuale debito inferiore a 25,82€).
Il risultato finale delle operazioni può essere un importo:

    * debito, da versare all'erario, se pari o superiore a 25,82 euro (altrimenti si riporta in aumento per il periodo successivo)
    * credito, da computare in detrazione nel periodo successivo.

::

    Destinatari:

Tutti i soggetti passivi IVA in regime non forfettario

::

    Normativa e prassi:

* `Articolo 23 del  DPR n. 633/72 - Registrazione fatture emesse <https://www.gazzettaufficiale.it/eli/id/1972/11/11/072U0633/sg>`__
* `Articolo 25 del  DPR n. 633/72 - Registrazione fatture degli acquisti <https://www.gazzettaufficiale.it/eli/id/1972/11/11/072U0633/sg>`__
* Articolo 39 del DPR n. 633/72 - Della tenuta e conservazione dei registri

Normativa non supportata da questo software:

* Articolo 24 del DPR n. 633/72) - Registrazione dei corrispettivi


|

Usage / Utilizzo
----------------

|en| In order to create a 'VAT Statement', open Accounting > Adviser > VAT Statements.
Select a Journal that will contain the journal entries of the statement.
The field Tax authority VAT account contains the account where the statement balance will be registered.

The 'VAT statement' object allows to specify every amount and relative account
used by the statement.
By default, amounts of debit and credit taxes are automatically loaded
from taxes of the selected periods (see Configuration to correctly generate the periods).
Previous debit or credit is loaded from previous VAT statement, according
to its payments status.

In order to generate the journal entry, click on 'Create move' button, inside the 'Accounts' tab.
If you select a payment term, the due date(s) will be set.

The 'tax authority' tab contains information about payment(s),
here you can see statement's result ('authority VAT amount') and residual
amount to pay ('Balance').
The statement can be paid like every other debit, by journal item
reconciliation.

It is also possible to print the 'VAT statement' clicking on print > Print VAT period end statement.

|it| Per fare la liquidazione IVA, aprire Contabilità > Contabilità > Liquidazioni IVA.
Selezionare un sezionale che conterrà le registrazioni contabili della liquidazione.
Il campo Conto IVA Erario contiene il conto dove verrà effettuata la registrazione della liquidazione IVA.

L'oggetto 'Liquidazione IVA' permette di specificare ogni importo e il conto utilizzato dalla liquidazione.
Di norma, gli importi di debito e credito delle tasse vengono caricati automaticamente dai periodi selezionati
(vedere Configurazione per generare correttamente i periodi).
I debiti e crediti precedenti vengono caricati dalle liquidazioni IVA precedenti, in base allo stato del loro pagamento.

Per creare la registrazione contabile, cliccare sul bottone 'Crea movimento', dentro il tab 'Conti'.
Se i termini di pagamento sono impostati viene scritta anche la scadenza (o le scadenze).

Il tab 'Erario' contiene informazioni sui pagamenti,
qui si possono visualizzare i risultati della liquidazione ('Importo IVA erario')
e l'importo residuo da pagare ('Importo a saldo').
La liquidazione può essere pagata come qualunque altro debito, con la riconciliazione delle registrazioni contabili.

È inoltre possibile stampare la liquidazione IVA cliccando su Stampa > Stampa liquidazione IVA.


|

OCA comparation / Confronto con OCA
-----------------------------------

+--------------------------------------------------+----------------------------------------------------------------+-------------------------------------------------------+--------------------------------------------------------------+
| Description / Descrizione                        |  OCA                                                           | Zeroincombenze                                        | Notes / Note                                                 |
+--------------------------------------------------+----------------------------------------------------------------+-------------------------------------------------------+--------------------------------------------------------------+
| Authority VAT account / Conto IVA erario         | Required / Obbligatorio                                        | Not required / Non obbligatorio                       | Il conto serve esclusivamente per la registrazione contabile |
+--------------------------------------------------+----------------------------------------------------------------+-------------------------------------------------------+--------------------------------------------------------------+
| Year footer                                      | |no_check|                                                     | |check|                                               | Come in 10.0                                                 |
+--------------------------------------------------+----------------------------------------------------------------+-------------------------------------------------------+--------------------------------------------------------------+
| Show zero rows / Mostra righe a zero             | |no_check|                                                     | |check|                                               | Mostra righe codici IVA con importo a zero                   |
+--------------------------------------------------+----------------------------------------------------------------+-------------------------------------------------------+--------------------------------------------------------------+
| Statement line fields  / Dati righe liquidazione | Importo IVA                                                    | Base imponibile, IVA, IVA detraibile                  |                                                              |
+--------------------------------------------------+----------------------------------------------------------------+-------------------------------------------------------+--------------------------------------------------------------+
| Data search / Ricerca dati                       | By supplemental VAT account in tax / Campo aggiuntivo in tasse | Based on VAT account in tax / Basato su Odoo standard |                                                              |
+--------------------------------------------------+----------------------------------------------------------------+-------------------------------------------------------+--------------------------------------------------------------+
| Multi-company                                    | Based on data range / Basato su intervalli date                | |check|                                               |                                                              |
+--------------------------------------------------+----------------------------------------------------------------+-------------------------------------------------------+--------------------------------------------------------------+


|
|

Getting started / Come iniziare
===============================

|Try Me|


|

Installation / Installazione
----------------------------


+---------------------------------+------------------------------------------+
| |en|                            | |it|                                     |
+---------------------------------+------------------------------------------+
| These instruction are just an   | Istruzioni di esempio valide solo per    |
| example to remember what        | distribuzioni Linux CentOS 7, Ubuntu 14+ |
| you have to do on Linux.        | e Debian 8+                              |
|                                 |                                          |
| Installation is built with:     | L'installazione è costruita con:         |
+---------------------------------+------------------------------------------+
| `Zeroincombenze Tools <https://github.com/zeroincombenze/tools>`__         |
+---------------------------------+------------------------------------------+
| Suggested deployment is:        | Posizione suggerita per l'installazione: |
+---------------------------------+------------------------------------------+
| /home/odoo/12.0/l10n-italy/                                                |
+----------------------------------------------------------------------------+

::

    cd $HOME
    git clone https://github.com/zeroincombenze/tools.git
    cd ./tools
    ./install_tools.sh -p
    source /opt/odoo/dev/activate_tools
    odoo_install_repository l10n-italy -b 12.0 -O zero
    venv_mgr create /opt/odoo/VENV-12.0 -O 12.0 -DI

From UI: go to:

|

Upgrade / Aggiornamento
-----------------------


+---------------------------------+------------------------------------------+
| |en|                            | |it|                                     |
+---------------------------------+------------------------------------------+
| When you want upgrade and you   | Per aggiornare, se avete installato con  |
| installed using above           | le istruzioni di cui sopra:              |
| statements:                     |                                          |
+---------------------------------+------------------------------------------+

::

    odoo_install_repository l10n-italy -b 12.0 -O zero -U
    venv_mgr amend /opt/odoo/VENV-12.0 -O 12.0 -DI
    # Adjust following statements as per your system
    sudo systemctl restart odoo

From UI: go to:

|

Support / Supporto
------------------


|Zeroincombenze| This module is maintained by the `SHS-AV s.r.l. <https://www.zeroincombenze.it/>`__


|
|

Get involved / Ci mettiamo in gioco
===================================

Bug reports are welcome! You can use the issue tracker to report bugs,
and/or submit pull requests on `GitHub Issues
<https://github.com/zeroincombenze/l10n-italy/issues>`_.

In case of trouble, please check there if your issue has already been reported.

Proposals for enhancement
-------------------------


|en| If you have a proposal to change this module, you may want to send an email to <cc@shs-av.com> for initial feedback.
An Enhancement Proposal may be submitted if your idea gains ground.

|it| Se hai proposte per migliorare questo modulo, puoi inviare una mail a <cc@shs-av.com> per un iniziale contatto.

|
|

Credits / Didascalie
====================

Copyright
---------

Odoo is a trademark of `Odoo S.A. <https://www.odoo.com/>`__ (formerly OpenERP)



|

Authors / Autori
----------------

* `Odoo Community Association (OCA) <https://odoo-community.org>`__
* `Associazione Odoo Italia <http://www.odoo-italia.org>`__
* `Agile Business Group sagl <http://www.agilebg.com>`__
* `SHS-AV s.r.l. <https://www.zeroincombenze.it/>`__


Contributors / Collaboratori
----------------------------

* Lorenzo Battistini <https://github.com/eLBati>
* Elena Carlesso
* Marco Marchiori <marcomarkiori@gmail.com>
* Sergio Corato <sergiocorato@gmail.com>
* Andrea Gallina <a.gallina@apuliasoftware.it>
* Alex Comba <alex.comba@agilebg.com>
* Alessandro Camilli <camillialex@gmail.com>
* Simone Rubino <simone.rubino@agilebg.com>
* Giacomo Grasso <giacomo.grasso.82@gmail.com>
* Lara Baggio <http://linkgroup.it/>
* Gianmarco Conte <gconte@dinamicheaziendali.it>
* Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>


|

----------------


|en| **zeroincombenze®** is a trademark of `SHS-AV s.r.l. <https://www.shs-av.com/>`__
which distributes and promotes ready-to-use **Odoo** on own cloud infrastructure.
`Zeroincombenze® distribution of Odoo <https://wiki.zeroincombenze.org/en/Odoo>`__
is mainly designed to cover Italian law and markeplace.

|it| **zeroincombenze®** è un marchio registrato da `SHS-AV s.r.l. <https://www.shs-av.com/>`__
che distribuisce e promuove **Odoo** pronto all'uso sulla propria infrastuttura.
La distribuzione `Zeroincombenze® <https://wiki.zeroincombenze.org/en/Odoo>`__ è progettata per le esigenze del mercato italiano.


|chat_with_us|


|

This module is part of l10n-italy project.

Last Update / Ultimo aggiornamento: 2020-06-24

.. |Maturity| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |Build Status| image:: https://travis-ci.org/zeroincombenze/l10n-italy.svg?branch=12.0
    :target: https://travis-ci.org/zeroincombenze/l10n-italy
    :alt: github.com
.. |license gpl| image:: https://img.shields.io/badge/licence-LGPL--3-7379c3.svg
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3
.. |license opl| image:: https://img.shields.io/badge/licence-OPL-7379c3.svg
    :target: https://www.odoo.com/documentation/user/9.0/legal/licenses/licenses.html
    :alt: License: OPL
.. |Coverage Status| image:: https://coveralls.io/repos/github/zeroincombenze/l10n-italy/badge.svg?branch=12.0
    :target: https://coveralls.io/github/zeroincombenze/l10n-italy?branch=12.0
    :alt: Coverage
.. |Codecov Status| image:: https://codecov.io/gh/zeroincombenze/l10n-italy/branch/12.0/graph/badge.svg
    :target: https://codecov.io/gh/zeroincombenze/l10n-italy/branch/12.0
    :alt: Codecov
.. |Tech Doc| image:: https://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-docs-12.svg
    :target: https://wiki.zeroincombenze.org/en/Odoo/12.0/dev
    :alt: Technical Documentation
.. |Help| image:: https://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-help-12.svg
    :target: https://wiki.zeroincombenze.org/it/Odoo/12.0/man
    :alt: Technical Documentation
.. |Try Me| image:: https://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-try-it-12.svg
    :target: https://erp12.zeroincombenze.it
    :alt: Try Me
.. |OCA Codecov| image:: https://codecov.io/gh/OCA/l10n-italy/branch/12.0/graph/badge.svg
    :target: https://codecov.io/gh/OCA/l10n-italy/branch/12.0
    :alt: Codecov
.. |Odoo Italia Associazione| image:: https://www.odoo-italia.org/images/Immagini/Odoo%20Italia%20-%20126x56.png
   :target: https://odoo-italia.org
   :alt: Odoo Italia Associazione
.. |Zeroincombenze| image:: https://avatars0.githubusercontent.com/u/6972555?s=460&v=4
   :target: https://www.zeroincombenze.it/
   :alt: Zeroincombenze
.. |en| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/flags/en_US.png
   :target: https://www.facebook.com/Zeroincombenze-Software-gestionale-online-249494305219415/
.. |it| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/flags/it_IT.png
   :target: https://www.facebook.com/Zeroincombenze-Software-gestionale-online-249494305219415/
.. |check| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/check.png
.. |no_check| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/no_check.png
.. |menu| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/menu.png
.. |right_do| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/right_do.png
.. |exclamation| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/exclamation.png
.. |warning| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/warning.png
.. |same| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/same.png
.. |late| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/late.png
.. |halt| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/halt.png
.. |info| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/info.png
.. |xml_schema| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/certificates/iso/icons/xml-schema.png
   :target: https://github.com/zeroincombenze/grymb/blob/master/certificates/iso/scope/xml-schema.md
.. |DesktopTelematico| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/certificates/ade/icons/DesktopTelematico.png
   :target: https://github.com/zeroincombenze/grymb/blob/master/certificates/ade/scope/Desktoptelematico.md
.. |FatturaPA| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/certificates/ade/icons/fatturapa.png
   :target: https://github.com/zeroincombenze/grymb/blob/master/certificates/ade/scope/fatturapa.md
.. |chat_with_us| image:: https://www.shs-av.com/wp-content/chat_with_us.gif
   :target: https://t.me/axitec_helpdesk

