# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

import ast


class RmaStageDelete(models.TransientModel):
    _name = 'rma.stage.delete.wizard'
    _description = 'RMA Stage Delete Wizard'

    stage_ids = fields.Many2many('rma.stage', string='Stages To Delete', ondelete='cascade')
    rma_count = fields.Integer('Number of RMA', compute='_compute_rma_count')
    stages_active = fields.Boolean(compute='_compute_stages_active')

    def _compute_rma_count(self):
        for wizard in self:
            wizard.rma_count = self.with_context(active_test=False).env['rma'].search_count(
                [('stage_id', 'in', wizard.stage_ids.ids)]
            )

    @api.depends('stage_ids')
    def _compute_stages_active(self):
        for wizard in self:
            wizard.stages_active = all(wizard.stage_ids.mapped('active'))

    def action_archive(self):
        if len(self.project_ids) <= 1:
            return self.action_confirm()

        return {
            'name': _('Confirmation'),
            'view_mode': 'form',
            'res_model': 'rma.stage.delete.wizard',
            'views': [(self.env.ref('rma_stage.view_rma_stage_delete_confirmation_wizard').id, 'form')],
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'target': 'new',
            'context': self.env.context,
        }

    def action_confirm(self):
        rmas = self.with_context(active_test=False).env['rma'].search([('stage_id', 'in', self.stage_ids.ids)])
        rmas.write({'active': False})
        self.stage_ids.write({'active': False})
        return self._get_action()

    def action_unlink(self):
        self.stage_ids.unlink()
        return self._get_action()

    def _get_action(self):
        action = self.env["ir.actions.actions"]._for_xml_id("rma.rma_action")

        context = dict(ast.literal_eval(action.get('context')), active_test=True)
        action['context'] = context
        action['target'] = 'main'
        return action
