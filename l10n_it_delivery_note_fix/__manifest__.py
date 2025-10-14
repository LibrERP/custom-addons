# © 2025 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'FIX - Documento di trasporto',
    'version': '16.0.0.3',
    'category': 'Localization/Italy',
    'summary': """Module take the name of the product in ddt from Sale Order Line,
    it also removes the block that forbids to invoice lines with 'order' invoice_policy""",
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'l10n_it_delivery_note_base',
        'l10n_it_delivery_note',
    ],
    'data': [
        'views/goods_appearance_views.xml'
    ],
}
