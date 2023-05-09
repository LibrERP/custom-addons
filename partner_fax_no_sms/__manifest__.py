# Copyright 2018 Apruzzese Francesco <f.apruzzese@apuliasoftware.it>
# Copyright 2020-2023 Andrei Levin <andrei.levin@didotech.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Partner fax',
    'version': '12.0.1.0.2',
    'category': 'Extra Tools',
    'summary': 'Add fax number on partner',
    'author': 'powERP enterprise network',
    'website': 'https://www.librerp.it',
    'development_status': 'Alpha',
    'license': 'LGPL-3',
    'depends': [
        'base_setup',
        'module_version',
    ],
    'data': ['views/res_partner.xml'],
    'installable': True,
}
