/** @odoo-module **/

import { registry } from "@web/core/registry";
import { kanbanView } from "@web/views/kanban/kanban_view";
import { KanbanController } from "@web/views/kanban/kanban_controller";
import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";
import { KanbanHeader } from "@web/views/kanban/kanban_header";
import { useService } from "@web/core/utils/hooks";

/**
 * Custom KanbanHeader for RMA that shows a delete wizard instead of
 * direct deletion when deleting RMA stages.
 */
export class RmaKanbanHeader extends KanbanHeader {
    setup() {
        super.setup();
        this.action = useService("action");
    }

    /**
     * Override deleteGroup to show wizard instead of confirmation dialog
     * when deleting RMA stages.
     */
    async deleteGroup() {
        const { group } = this.props;
        // Check if this is an RMA stage group (model is 'rma' grouped by 'stage_id')
        const resModel = group.groupByField?.relation;
        if (resModel === "rma.stage") {
            // Call the unlink_wizard method instead of direct deletion
            const action = await this.orm.call(
                "rma.stage",
                "unlink_wizard",
                [[group.value]],
                { context: group.context }
            );
            if (action) {
                this.action.doAction(action, {
                    onClose: async () => {
                        // Reload the view after the wizard is closed
                        await this.props.list.load();
                        this.props.list.model.notify();
                    }
                });
            }
        } else {
            // For other models, use the default behavior
            super.deleteGroup();
        }
    }
}

/**
 * Custom KanbanRenderer that uses RmaKanbanHeader for RMA views.
 */
export class RmaKanbanRenderer extends KanbanRenderer {
    static components = {
        ...KanbanRenderer.components,
        KanbanHeader: RmaKanbanHeader,
    };
}

/**
 * RMA Kanban View definition
 */
export const rmaKanbanView = {
    ...kanbanView,
    Renderer: RmaKanbanRenderer,
};

// Register the custom view
registry.category("views").add("rma_kanban", rmaKanbanView);
