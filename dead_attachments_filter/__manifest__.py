# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Tools: Remove Dead Attachments',
    'version': '16.0.0.0',
    'category': 'tools',
    'summary': 'Clean database from dead attachments',
    'author': 'Codebeex srl',
    'website': 'https://github.com/LibrERP/custom-addons',
    'license': 'AGPL-3',
    'depends': [
        'base',
    ],
    'data': [
        'views/ir_attachment_views.xml'
    ],
}
