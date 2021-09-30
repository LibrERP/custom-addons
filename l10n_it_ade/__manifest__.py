# -*- coding: utf-8 -*-
# Copyright 2018 - Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#                  Associazione Odoo Italia <http://www.odoo-italia.org>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Code partially inherited by l10n_it_account of OCA
#
{
    'name': 'Base xml Agenzia delle Entrate',
    'version': '12.0.0.1.10',
    'category': 'Localization/Italy',
    'summary': 'Codice con le definizioni dei file xml Agenzia delle Entrate',
    'author': 'powERP enterprise network, SHS-AV s.r.l.',
    'website': 'https://www.powerp.it',
    'development_status': 'Alpha',
    'license': 'LGPL-3',
    'depends': ['account'],
    'external_dependencies': {'python': ['pyxb']},
    'data': [
        'security/ir.model.access.csv',
        'data/italy_ade_tax_nature.xml',
        'data/italy_ade_codice_carica.xml',
        'data/italy_ade_invoice_type.xml',
        'views/ir_ui_menu.xml',
        'views/account_tax_view.xml',
        'views/account_journal.xml',
        'views/codice_carica_view.xml',
        'views/tax_nature_view.xml',
        'views/invoice_type_view.xml',
    ],
    'maintainer': 'powERP enterprise network',
    'installable': False,
}
