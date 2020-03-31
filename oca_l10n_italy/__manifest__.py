# -*- coding: utf-8 -*-
# © 2020 Andrei Levin (Didotech s.r.l.)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'l10n_italy correction',
    'summary': "Correction for modules in l10n_italy",
    'version': '12.0.0.0.0',
    'category': 'Localisation/Italy',
    'depends': [
        'base',
        'l10n_it_fiscalcode'    # OCA l10n_italy
    ],
    'author': """
        Andrei Levin
    """,
    'website': 'https://github.com/LibrERP/custom-addons',
    'license': 'AGPL-3',
    'data': [
        'views/partner_view.xml',
        'wizard/compute_fc_view.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
