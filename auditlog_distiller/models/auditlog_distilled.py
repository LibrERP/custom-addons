# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models
import datetime


class AuditlogDistilled(models.Model):
    _name = "auditlog.distilled"
    _description = "A distilled version of auditlog_log table"

    name = fields.Char()
    model_id = fields.Many2one(
        'ir.model', string="Model")
    res_id = fields.Integer("Resource ID")
    user_id = fields.Many2one('res.users', string="User")
    method = fields.Selection([
        ('create', 'Create'),
        ('write', 'Write'),
        ('unlink', 'Delete'),
        ('read', 'Read')
    ])
    log_date = fields.Datetime()

    def distill(self, row):
        # Tolerance in seconds
        tolerance = 12
        end_date = row.create_date + datetime.timedelta(seconds=tolerance)

        last_log = self.env['auditlog.log'].search_read([
            ('user_id', '=', row.user_id.id),
            ('create_date', '>=', row.create_date),
            ('create_date', '<', end_date),
        ], ('id', 'name', 'create_date'), limit=1, order='id desc')[0]

        self.create({
            'name': row.name,
            'model_id': row.model_id.id,
            'res_id': row.res_id,
            'user_id': row.user_id.id,
            'method': row.method,
            'log_date': last_log.create_date
        })

        return last_log

    def distiller(self):
        # This method is called periodically to create distilled logs

        start = self.env['auditlog.distilled'].search_read([], ('create_date',), limit=1, order='id desc')

        if start:
            row = self.env['auditlog.log'].search([('create_date', '>', start[0]['create_date'])], limit=1, order='id')
        else:
            row = self.env['auditlog.log'].search([], limit=1, order='id')

        while row:
            last_log = self.distill(row)
            row = self.env['auditlog.log'].search([('id', '>', last_log['id'])], limit=1, order='id')
