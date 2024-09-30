odoo.define('web_onchange_wizard.BasicModel', function (require) {
'use strict';

    var BasicModel = require('web.BasicModel');

    /* override to return action from onchange */
    BasicModel.include({
        
        _performOnChange: function (record, fields, viewType) {
            var self = this;
            var onchangeSpec = this._buildOnchangeSpecs(record, viewType);
            if (!onchangeSpec) {
                return $.when();
            }
            var idList = record.data.id ? [record.data.id] : [];
            var options = {
                full: true,
            };
            if (fields.length === 1) {
                fields = fields[0];
                // if only one field changed, add its context to the RPC context
                options.fieldName = fields;
            }
            var context = this._getContext(record, options);
            var currentData = this._generateOnChangeData(record, {changesOnly: false});
    
            return self._rpc({
                    model: record.model,
                    method: 'onchange',
                    args: [idList, currentData, fields, onchangeSpec, context],
                })
                .then(function (result) {
                    if (!record._changes) {
                        // if the _changes key does not exist anymore, it means that
                        // it was removed by discarding the changes after the rpc
                        // to onchange. So, in that case, the proper response is to
                        // ignore the onchange.
                        return;
                    }
                    if (result.warning) {
                        self.trigger_up('warning', {
                            message: result.warning.message,
                            title: result.warning.title,
                            type: 'dialog',
                        });
                        record._warning = true;
                    }
                    // allow to perform action
                    if (result.action) {
                        self.do_action(result.action);
                    }
                    if (result.domain) {
                        record._domains = _.extend(record._domains, result.domain);
                    }
                    return self._applyOnChange(result.value, record).then(function () {
                        return result;
                    });
                });
        },
    });

});