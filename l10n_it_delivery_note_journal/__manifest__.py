# © 2025 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Documento di trasporto - Registro',
    'version': '16.0.0.0',
    'category': 'Localization/Italy',
    'summary': 'Module adds a possibility to select journal during invoice creation from delivery note',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'sale',
        'l10n_it_delivery_note'
    ],
    'data': [
        'wizard/delivery_note_invoice.xml'
    ],
}
