# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models
from odoo.addons.auditlog.models.rule import DictDiffer

EMPTY_DICT = {}


class AuditlogRule(models.Model):
    _inherit = 'auditlog.rule'

    def create_logs(self, uid, res_model, res_ids, method,
                    old_values=None, new_values=None,
                    additional_log_values=None):
        """Create logs. `old_values` and `new_values` are dictionaries, e.g:
            {RES_ID: {'FIELD': VALUE, ...}}
        """
        if old_values is None:
            old_values = EMPTY_DICT
        if new_values is None:
            new_values = EMPTY_DICT
        log_model = self.env['auditlog.log']
        http_request_model = self.env['auditlog.http.request']
        http_session_model = self.env['auditlog.http.session']

        model_model = self.env[res_model]

        if res_model in self.pool._auditlog_model_cache:
            model_id = self.pool._auditlog_model_cache[res_model]
        else:
            model_id = self.env['ir.model'].search_read([('model', '=', res_model)], ('id',), limit=1)[0]['id']

        auditlog_rule = self.env['auditlog.rule'].search(
            [("model_id", "=", model_id)])

        for res_id in res_ids:
            name = model_model.browse(res_id).name_get()
            res_name = name and name[0] and name[0][1]
            vals = {
                'name': res_name,
                'model_id': model_id,
                'res_id': res_id,
                'method': method,
                'user_id': uid,
                'http_request_id': http_request_model.current_http_request(),
                'http_session_id': http_session_model.current_http_session(),
            }
            vals.update(additional_log_values or {})
            log = log_model.create(vals)
            diff = DictDiffer(
                new_values.get(res_id, EMPTY_DICT),
                old_values.get(res_id, EMPTY_DICT))
            if method is 'create':
                self._create_log_line_on_create(log, diff.added(), new_values)
            elif method is 'read':
                self._create_log_line_on_read(
                    log,
                    list(old_values.get(res_id, EMPTY_DICT).keys()), old_values
                )
            elif method is 'write':
                self._create_log_line_on_write(
                    log, diff.changed(), old_values, new_values)
            elif method is 'unlink' and auditlog_rule.capture_record:
                self._create_log_line_on_read(
                    log,
                    list(old_values.get(res_id, EMPTY_DICT).keys()), old_values
                )
