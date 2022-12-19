# © 2022 Marco Tosato - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Add new search criterias to l10n_it_fatturapa_in',
    'version': '12.0.1.0.1',
    'category': 'Localisation/Italy',
    'summary': 'New searches: invoice number, VAT number, Fiscal Code',
    'author': 'LibrERP enterprise network',
    'website': 'https://www.librerp.it',
    'development_status': 'Alpha',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'l10n_it_fatturapa_in',
        'l10n_it_efattura_in_extra_data_loading_infra',
    ],
    'data': [
        'views/fatturapa_attachment_in_search.xml',
    ],
    'demo': [
    ],
}
