# © 2025 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Auditlog Distilled',
    'version': '12.0.0.0',
    'category': 'Tools',
    'summary': 'Module create a table from auditlog_log where rows of the same task are united',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'mail',
        'auditlog'  # OCA/server-tools
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        # 'views/xxx_views.xml'
    ],
}
