# Copyright 2018 Apruzzese Francesco <f.apruzzese@apuliasoftware.it>
# Copyright 2020-2023 Andrei Levin <andrei.levin@didotech.com>
# Copyright 2023-2026 Andrei Levin <andrei.levin@codebeex.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Partner fax',
    'version': '12.0.1.0.3',
    'category': 'Extra Tools',
    'summary': 'Add fax number on partner',
    'author': 'powERP enterprise network',
    'website': 'https://www.codebeex.com',
    'development_status': 'Alpha',
    'license': 'LGPL-3',
    'depends': [
        'base_setup',
        'module_version',
    ],
    'data': ['views/res_partner.xml'],
    'installable': True,
    'post_init_hook': 'check_incompatible_modules',
}
