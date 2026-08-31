# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, SUPERUSER_ID
from odoo.exceptions import UserError


def check_incompatible_modules(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})

    modules = env['ir.module.module'].search([
        ('name', '=', 'sms'),
        ('state', 'in', ['installed', 'to upgrade'])
    ])

    if modules:
        raise UserError(
            "Module 'partner_fax_no_sms' is incompatible with 'sms'.\n"
            "Use 'partner_fax' instead or uninstall 'sms'."
        )
