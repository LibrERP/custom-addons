# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models, SUPERUSER_ID


class RmaStage(models.Model):
    _name = 'rma.stage'
    _description = 'RMA Stage'
    _order = 'sequence, id'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='Stage Name', required=True, translate=True)
    description = fields.Text(translate=True)
    sequence = fields.Integer(default=1)
    # legend_blocked = fields.Char(
    #     'Red Kanban Label', default=lambda s: _('Blocked'), translate=True, required=True,
    #     help='Override the default value displayed for the blocked state for kanban selection, when the task or issue is in that stage.')
    # legend_done = fields.Char(
    #     'Green Kanban Label', default=lambda s: _('Ready'), translate=True, required=True,
    #     help='Override the default value displayed for the done state for kanban selection, when the task or issue is in that stage.')
    # legend_normal = fields.Char(
    #     'Grey Kanban Label', default=lambda s: _('In Progress'), translate=True, required=True,
    #     help='Override the default value displayed for the normal state for kanban selection, when the task or issue is in that stage.')
    fold = fields.Boolean(string='Folded in Kanban',
        help='This stage is folded in the kanban view when there are no records in that stage to display.')
    is_closed = fields.Boolean('Closing Stage', help="RMA in this stage are considered as closed.")

    def unlink_wizard(self, stage_view=False):
        self = self.with_context(active_test=False)
        # retrieves all the projects with a least 1 task in that stage
        # a task can be in a stage even if the project is not assigned to the stage

        wizard = self.env['rma.stage.delete.wizard'].create({
            'stage_ids': self.ids
        })

        context = dict(self.env.context)
        context['stage_view'] = stage_view
        return {
            'name': _('Delete Stage'),
            'view_mode': 'form',
            'res_model': 'rma.stage.delete.wizard',
            'views': [(self.env.ref('project.view_project_task_type_delete_wizard').id, 'form')],
            'type': 'ir.actions.act_window',
            'res_id': wizard.id,
            'target': 'new',
            'context': context,
        }


class Rma(models.Model):
    _inherit = "rma"

    def _get_default_stage_id(self):
        """ Gives default stage_id """
        order = 'sequence'
        search_domain = [('fold', '=', False), ('is_closed', '=', False)]
        return self.env['rma.stage'].search(search_domain, order=order, limit=1).id

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        # search_domain = [('id', 'in', stages.ids)]
        search_domain = []
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Important'),
    ], default='0', index=True, string="Priority")
    stage_id = fields.Many2one(
        'rma.stage', string='Stage', readonly=False, ondelete='restrict',
        tracking=True, index=True,
        default=_get_default_stage_id, group_expand='_read_group_stage_ids',
        copy=False
    )
    kanban_state = fields.Selection([
        ('normal', 'In Progress'),
        ('done', 'Ready'),
        ('blocked', 'Blocked')], string='Kanban State',
        copy=False, default='normal', required=True)
    # kanban_state_label = fields.Char(compute='_compute_kanban_state_label', string='Kanban State Label', tracking=True)
    #
    # legend_blocked = fields.Char(related='stage_id.legend_blocked', string='Kanban Blocked Explanation', readonly=True,
    #                              related_sudo=False)
    # legend_done = fields.Char(related='stage_id.legend_done', string='Kanban Valid Explanation', readonly=True,
    #                           related_sudo=False)
    # legend_normal = fields.Char(related='stage_id.legend_normal', string='Kanban Ongoing Explanation', readonly=True,
    #                             related_sudo=False)
    is_closed = fields.Boolean(related="stage_id.is_closed", string="Closing Stage", readonly=True, related_sudo=False)
    color = fields.Integer(string='Color Index')
    sequence = fields.Integer(default=1)

    # @api.depends('stage_id', 'kanban_state')
    # def _compute_kanban_state_label(self):
    #     for rma in self:
    #         if rma.kanban_state == 'normal':
    #             rma.kanban_state_label = rma.legend_normal
    #         elif rma.kanban_state == 'blocked':
    #             rma.kanban_state_label = rma.legend_blocked
    #         else:
    #             rma.kanban_state_label = rma.legend_done