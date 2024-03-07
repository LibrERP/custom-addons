# © 2024 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Budget Expected',
    'version': '16.0.0.5',
    'category': 'Accounting/Accounting',
    'summary': "Add Expected column to the Budget. "
               "It's content is based on Sale and Purchase Order valued",
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account_budget',
        'project_enterprise',
        'project_account_budget'
    ],
    'data': [
        'views/budget_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'account_budget_expected/static/src/components/**/*',
        ],
    },
}
