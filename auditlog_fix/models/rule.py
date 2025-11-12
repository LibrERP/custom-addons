# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import copy

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

    @api.multi
    def _make_create(self):
        """Instanciate a create method that log its calls."""
        self.ensure_one()
        log_type = self.log_type

        @api.model_create_multi
        @api.returns('self', lambda value: value.id)
        def create_full(self, vals_list, **kwargs):
            self = self.with_context(auditlog_disabled=True)
            rule_model = self.env['auditlog.rule']
            new_records = create_full.origin(self, vals_list, **kwargs)
            # Take a snapshot of record values from the cache instead of using
            # 'read()'. It avoids issues with related/computed fields which
            # stored in the database only at the end of the transaction, but
            # their values exist in cache.
            new_values = {}
            fields_list = rule_model.get_auditlog_fields(self)
            for new_record in new_records.sudo():
                new_values.setdefault(new_record.id, {})
                for fname, field in new_record._fields.items():
                    if fname not in fields_list:
                        continue
                    new_values[new_record.id][fname] = field.convert_to_read(
                        new_record[fname], new_record)
            rule_model.sudo().create_logs(
                self.env.uid, self._name, new_records.ids,
                'create', None, new_values, {'log_type': log_type})
            return new_records

        def remove_recordsets(data):
            if isinstance(data, dict):
                return {k: remove_recordsets(v) for k, v in data.items()}
            elif isinstance(data, list):
                return [remove_recordsets(v) for v in data]
            elif hasattr(data, '_name'):  # Odoo recordset
                return None
            return data

        @api.model_create_multi
        @api.returns('self', lambda value: value.id)
        def create_fast(self, vals_list, **kwargs):
            self = self.with_context(auditlog_disabled=True)
            rule_model = self.env['auditlog.rule']
            vals_list2 = copy.deepcopy(remove_recordsets(vals_list))
            new_records = create_fast.origin(self, vals_list, **kwargs)
            new_values = {}
            for vals, new_record in zip(vals_list2, new_records):
                new_values.setdefault(new_record.id, vals)
            rule_model.sudo().create_logs(
                self.env.uid, self._name, new_records.ids,
                'create', None, new_values, {'log_type': log_type})
            return new_records

        return create_full if self.log_type == 'full' else create_fast
