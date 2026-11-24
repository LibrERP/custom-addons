# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Helpdesk Sale Timesheet Fix',
    'version': '18.0.1.0.1',
    'category': 'Services/Helpdesk',
    'summary': 'Do not link Helpdesk tickets automatically to a random Sales Order Item of the customer',
    'author': 'Codebeex srl',
    'website': 'https://github.com/LibrERP/custom-addons',
    'license': 'AGPL-3',
    'depends': [
        'helpdesk_sale_timesheet',  # Enterprise
    ],
    'data': [],
    'installable': True,
    'auto_install': False,
}
