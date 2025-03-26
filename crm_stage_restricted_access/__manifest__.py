# © 2025 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'CRM Stage restricted access',
    'version': '12.0.0.0',
    'category': 'crm',
    'summary': 'Gain full access to crm stage to a dedicated group',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'crm'
    ],
    'data': [
        'security/crm_stage_security.xml'
    ],
}
