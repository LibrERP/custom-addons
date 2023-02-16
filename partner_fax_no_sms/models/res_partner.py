# Copyright 2018 Apruzzese Francesco <f.apruzzese@apuliasoftware.it>
# Copyright 2020-2023 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
from odoo.exceptions import Warning
from odoo import http


class ResPartner(models.Model):
    _inherit = 'res.partner'

    fax = fields.Char()


# This code should be in the end of the file
result = http.request.cr.execute("SELECT name FROM ir_module_module WHERE state IN ('installed', 'to upgrade')")
modules = http.request.cr.dictfetchall()
modules = [module['name'] for module in modules if 'sms' in module['name'] and not module['name'] == 'partner_fax_no_sms']
if 'sms' in modules:
    raise Warning("""module 'partner_fax_no_sms is incompatible with module 'SMS gateway'
    Use module 'partner_fax' instead or uninstall 'sms' module""")
