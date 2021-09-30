# © 2021 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'l10n_it_ddt_detach',
    'version': '12.0.0.1',
    'category': 'Accounting',
    'summary': 'Detach Invoice from TD',
    'author': 'SHS-AV s.r.l.',
    'website': 'https://www.zeroincombenze.it',
    'development_status': 'Alpha',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account',
        'l10n_it_ddt',
    ],
    'external_dependencies': {},
    'data': [
        'wizard/wizard_detach_invoice_view.xml',
        'views/stock_picking_package_preparation_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
