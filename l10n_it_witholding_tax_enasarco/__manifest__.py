# Copyright 2023 Didotech s.r.l. https://www.didotech.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': "ITA - Ritenuta d'acconto - Pagamenti Enasarco",
    'summary': "Gestisce le ritenute sulle fatture con enasarco e sui pagamenti",
    'version': '12.0.1.0.1',
    'development_status': "Beta",
    'category': "Invoicing & Payments",
    'website': 'https://www.didotech.com',
    'author': "Didotech s.r.l., ",
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'account',
        'l10n_it_withholding_tax'
    ],
    'data': []
}
