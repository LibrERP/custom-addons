# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    ddt_note = fields.Text('DDT Note', help=_("This note will be printed in the DDT"))
    ddt_internal_note = fields.Text('DDT Internal Note', help=_("This note is not printed in the DDT"))

    @api.model
    def create(self, values):
        if values.get('partner_id', False):
            partner = self.env['res.partner'].browse(values['partner_id'])
            values['ddt_internal_note'] = partner.ddt_internal_note
            values['ddt_note'] = partner.ddt_note

        return super().create(values)

    def write(self, values):
        if values.get('partner_id', False):
            partner = self.env['res.partner'].browse(values['partner_id'])
            values['ddt_internal_note'] = partner.ddt_internal_note
            values['ddt_note'] = partner.ddt_note

        return super().write(values)

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        self.ddt_note = self.partner_id.ddt_note
        self.ddt_internal_note = self.partner_id.ddt_internal_note


class StockPickingPackagePreparation(models.Model):
    _inherit = 'stock.picking.package.preparation'

    ddt_note = fields.Text('DDT Note', help=_("This note will be printed in the DDT"))
    ddt_internal_note = fields.Text('DDT Internal Note', help=_("This note is not printed in the DDT"))

    @api.model
    def create(self, values):
        if self._context['active_model'] == 'stock.picking':
            pickings = self.env['stock.picking'].browse(self._context['active_ids'])
            values['ddt_internal_note'] = pickings[0].ddt_internal_note
            values['ddt_note'] = pickings[0].ddt_note
        elif values.get('partner_id', False):
            partner = self.env['res.partner'].browse(values['partner_id'])
            values['ddt_internal_note'] = partner.ddt_internal_note
            values['ddt_note'] = partner.ddt_note

        return super().create(values)

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        self.ddt_note = self.partner_id.ddt_note
        self.ddt_internal_note = self.partner_id.ddt_internal_note
