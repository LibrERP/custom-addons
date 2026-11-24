# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Helpdesk Ticket Deduplicate',
    'version': '18.0.1.0.0',
    'category': 'Services/Helpdesk',
    'summary': 'Warn on, and filter, tickets created twice from the same email (e.g. sent to two helpdesk aliases)',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'helpdesk',  # Enterprise
        'account',  # x2many_buttons widget, as in the account.move duplicate warning
    ],
    'data': [
        'views/helpdesk_ticket_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
