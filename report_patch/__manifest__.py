# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Report Patch (fix multipage problem)',
    'version': '18.0.0.0',
    'category': 'core',
    'summary': 'This patch solve the problem with _render_qweb_pdf_prepare_streams() returning '
               'a merged PDF instead of falling back to individual rendering when /Outlines is absent.',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
    ],
    'data': [],
}
