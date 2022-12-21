# © 2022 Marco Tosato - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'E-Fattura In: document type',
    'version': '12.0.1.1.2',
    'category': 'Localisation/Italy',
    'summary': 'Show document type from XML in the tree view',
    'author': 'LibrERP enterprise network',
    'website': 'https://www.librerp.it',
    'development_status': 'Alpha',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'l10n_it_fatturapa_in',
        'l10n_it_fatturapa_in_extra_data_loading_infra',
    ],
    'data': [
        'views/fatturapa_attachment_in.xml',
    ],
    'demo': [
    ],
}
