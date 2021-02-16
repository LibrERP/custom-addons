# Copyright 2021 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Partner VAT search',
    'category': 'Extra Tools',
    'summary': 'Add vat search on partner',
    'version': '12.0.0.1',
    'license': 'AGPL-3',
    'author':  'Didotech srl',
    'website': 'https://github.com/LibrERP/custom-addons',
    'depends': [
        'base'
    ],
    'data': [
        'views/res_partner_view.xml'
    ],
    'installable': True,
}
