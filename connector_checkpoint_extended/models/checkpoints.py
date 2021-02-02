# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ConnectorCheckpoint(models.Model):
    _inherit = 'connector.checkpoint'

    message = fields.Text(string="Message", required=False)

    @api.model
    def create_from_name_with_message(self, model_name, record_id,
                         backend_model_name, backend_id, message):
        model_model = self.env['ir.model']
        model = model_model.search([('model', '=', model_name)], limit=1)
        assert model, "The model %s does not exist" % model_name
        backend = backend_model_name + ',' + str(backend_id)
        return self.create({
            'model_id': model.id,
            'record_id': record_id,
            'backend_id': backend,
            'message': message
        })
