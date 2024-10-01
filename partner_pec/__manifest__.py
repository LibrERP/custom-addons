# © 2024 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
#
# README.rst generation:
# oca-gen-addon-readme --repo-name=custom-addons --branch=16.0 --addon-dir=partner_pec --org-name=LibrERP
{
    'name': 'Partner PEC',
    'version': '16.0.0.1',
    'category': 'Extra Tools',
    'summary': 'Add PEC field on partner',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    # "excludes": [
    #     "l10n_it_edi"
    # ],
    'depends': [
        'base_setup',
    ],
    'data': [
        'views/partner_views.xml'
    ],
    "installable": True,
}
