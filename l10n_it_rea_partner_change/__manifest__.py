# © 2025 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'No REA check when changing Partner Name',
    'version': '16.0.0.0',
    'category': 'Localisation/Italy',
    'summary': """To change partner's name we need first create a copy of the partner 
                so the historic name will be preserved. 
                There is a check that prevents from having duplicated rea codes inside the same database.
                This module will suppress the check for partners that are just versions of the same partner""",
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'l10n_it_rea',
        'partner_history'
    ],
    'data': [
        # 'views/xxx_views.xml'
    ],
}
