# Copyright 2023 Didotech  <https://www.didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'ITA - Nota di credito da DDT reso a fornitore',
    'version': '12.0.1.0.2',
    'category': 'Localization/Italy',
    'summary': 'Reso a fornitore',
    'author': 'Didotech srl',
    'website': 'https://www.didotech.com',
    'license': 'AGPL-3',
    'depends': [
        'stock',
        'l10n_it_ddt',
    ],
    'data': [
        'wizard/ddt_creditnote.xml',
        'views/stock_picking_package_preparation.xml',
    ],
    'installable': True
}
