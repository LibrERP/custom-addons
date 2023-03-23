# -*- coding: utf-8 -*-
# © 2013-2021 Didotech srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo import exceptions


class Module(models.Model):
    _inherit = "ir.module.module"

    def _check_upgrade(self):
        installed_modules = self.search([('state', 'in', ['installed', 'to upgrade', 'to remove'])])
        for module in installed_modules:
            # if module.name == 'module_version':
            #     print module.name
            #     pdb.set_trace()
            if not module.latest_version == self.get_module_info(module.name).get('version', '') and not module.need_upgrade:
                # module.need_upgrade = True
                module.write({'need_upgrade': True})
            elif module.latest_version == self.get_module_info(module.name).get('version', '') and module.need_upgrade:
                module.need_upgrade = False

    @api.depends('installed_version', 'latest_version')
    def _need_upgrade(self):
        for module in self:
            if module.state in ['installed', 'to upgrade', 'to remove'] and not module.latest_version == module.get_module_info(module.name).get('version', ''):
                module.need_upgrade = True
            else:
                module.need_upgrade = False

    need_upgrade = fields.Boolean(compute='_need_upgrade', string=_('Need Upgrade'), store=True)
    check_upgrade = fields.Boolean(compute='_check_upgrade', string=_('Need Upgrade (hidden)'), store=False)

    _order = 'name'

    @property
    @api.model
    def installed_modules(self):
        return self.search([('state', 'in', ['installed', 'to upgrade', 'to remove'])])

    @api.model
    def set_modules_to_upgrade(self, view=False):
        modules = self.env['ir.module.module']

        # installed_modules = self.search([('state', 'in', ['installed', 'to upgrade', 'to remove'])])
        for module in self.installed_modules:
            if not module.latest_version == self.get_module_info(module.name).get('version', '') or module.state in ('to upgrade', 'to remove'):
                modules += module

        if modules:
            modules.button_upgrade()
            if view:
                return modules
            else:
                return True
        else:
            return False

    def verify_modules(self):
        modules = self.set_modules_to_upgrade(view=True)
        if modules:
            return {
                'type': 'ir.actions.act_window',
                'name': _('Modules to upgrade'),
                'res_model': 'ir.module.module',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'view_id': False,
                'target': 'current',
                'res_id': False,
                "domain": [('id', 'in', modules.ids)]
            }
        else:
            raise exceptions.UserError(_('There are no modules that should be updated'))

    def _button_immediate_function(self, function):
        super(Module, self)._button_immediate_function(function)
        return {
            'type': 'ir.actions.client',
            'tag': 'reload'
        }
