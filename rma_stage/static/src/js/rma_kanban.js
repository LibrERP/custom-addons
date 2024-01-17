odoo.define('rma_stage.rma_kanban', function (require) {
'use strict';

var KanbanController = require('web.KanbanController');
var KanbanView = require('web.KanbanView');
var KanbanColumn = require('web.KanbanColumn');
var view_registry = require('web.view_registry');
var KanbanRecord = require('web.KanbanRecord');

var RmaKanbanController = KanbanController.extend({
//    custom_events: _.extend({}, KanbanController.prototype.custom_events, {
//        'kanban_column_delete_wizard': '_onDeleteColumnWizard',
//    }),
//
//    _onDeleteColumnWizard: function (ev) {
//        ev.stopPropagation();
//        const self = this;
//        const column_id = ev.target.id;
//        var state = this.model.get(this.handle, {raw: true});
//        this._rpc({
//            model: 'rma.stage',
//            method: 'unlink_wizard',
//            args: [column_id],
//            context: state.getContext(),
//        }).then(function (res) {
//            self.do_action(res);
//        });
//    }
});

var RmaKanbanView = KanbanView.extend({
    config: _.extend({}, KanbanView.prototype.config, {
        Controller: RmaKanbanController
    }),
});

KanbanColumn.include({
    _onDeleteColumn: function (event) {
        if (this.modelName === 'rma' && this.groupedBy === 'stage_id') {
            event.preventDefault();
            this.trigger_up('kanban_column_delete_wizard');
            return;
        }
        this._super.apply(this, arguments);
    }
});

view_registry.add('rma_kanban', RmaKanbanView);

return RmaKanbanController;
});
