# © 2024 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'ITA - Emissione e-fattura con reverse charge FIX',
    'version': '16.0.0.1',
    'category': 'Hidden',
    'summary': 'Set Cessionario/committente to My Company in case of Reverse Charge',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'l10n_it_fatturapa_out'
    ],
    'data': [
        'views/invoice_it_template.xml'
    ],
}
