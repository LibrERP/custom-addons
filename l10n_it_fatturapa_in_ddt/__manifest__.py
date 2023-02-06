# © 2022-2023 Marco Tosato - Didotech srl (www.didotech.com)
# License OPL-1.0 or later (https://www.odoo.com/documentation/12.0/legal/licenses/licenses.html).
{
    'name': 'E-Fattura In: DDT collegati',
    'version': '12.0.9.7.3',
    'category': 'Generic Modules/Accounting',
    'summary': '',
    'author': 'LibrERP enterprise network',
    'website': 'https://www.librerp.it',
    'development_status': 'Alpha',
    'license': 'OPL-1',
    'depends': [
        'base',
        'l10n_it_ddt',
        'l10n_it_fatturapa_in',
        'l10n_it_fatturapa_in_extra_data_loading_infra',
    ],
    'data': [
        'views/attachment_view.xml',
    ],
    'description': '',
}
