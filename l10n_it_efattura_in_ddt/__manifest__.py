# License OPL-1.0 or later (https://www.odoo.com/documentation/12.0/legal/licenses/licenses.html).
{
    'name': 'Fattura Elettronica In - DDT collegati',
    'version': '12.0.4.0.2',
    'category': 'Generic Modules/Accounting',
    'summary': '',
    'author': 'powERP enterprise network',
    'website': 'https://www.powerp.it',
    'development_status': 'Alpha',
    'license': 'OPL-1',
    'depends': [
        'base',
        'l10n_it_ddt',
        'l10n_it_fatturapa_in',
        'l10n_it_efattura_in_extra_data_loading_infra',
    ],
    'data': [
        'views/attachment_view.xml',
    ],
    'description': '',
}
