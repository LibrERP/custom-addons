/** @odoo-module **/

import { KanbanController } from "@web/views/kanban/kanban_controller";
import { kanbanView } from "@web/views/kanban/kanban_view";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

class ProjectTaskOpenProjectController extends KanbanController {
    setup() {
        super.setup();
        this.action = useService("action");
        this.notification = useService("notification");
    }

    async openProject() {
        await this.model.load();

        let selectedResIds = this.model.root.selection.map(localId => {
            const record = this.model.root.records.find(r => r.id === localId);
            return record ? record.resId : null;
        }).filter(Boolean);

        let projectId = null;
        let projectName = null;

        if (selectedResIds.length) {
            // With selection: let server action handle (it will validate single project)
            this.action.doAction("project_view_from_task.action_server_view_project_from_task", {
                additionalContext: {
                    active_model: "project.task",
                    active_ids: selectedResIds,
                },
            });
            return;
        }

        // No selection: try tasks first
        const records = this.model.root.records;
        if (records.length) {
            const projectIds = [...new Set(records.map(r => r.data.project_id).filter(Boolean).map(p => p?.[0]))];
            if (projectIds.length === 1) {
                projectId = projectIds[0];
                projectName = records.find(r => r.data.project_id?.[0] === projectId)?.data.project_id[1];
            } else if (projectIds.length > 1) {
                this.notification.add(_t("Tasks belong to multiple projects"), { type: "warning" });
                return;
            }
            // If no project in tasks, fall through to context
        }

        // Fallback: parent project from context (e.g., opened from Project form)
        const parentContext = this.env.config.context || {};
        if (parentContext.active_model === "project.project" && parentContext.active_id) {
            projectId = parentContext.active_id;
            // Optional: fetch name if needed, but action can handle res_id
        } else if (!projectId && !records.length) {
            this.notification.add(_t("No tasks found, no way to find parent project"), { type: "warning" });
            return;
        }

        if (projectId) {
            this.action.doAction({
                type: "ir.actions.act_window",
                res_model: "project.project",
                res_id: projectId,
                views: [[false, "form"]],
                target: "current",
                name: projectName || _t("Project"),
            });
            return;
        }

        // Ultimate fallback: trigger server action with no ids (it will show "No tasks selected")
        this.action.doAction("project_view_from_task.action_server_view_project_from_task", {
            additionalContext: {
                active_model: "project.task",
                active_ids: [],
            },
        });
    }
}

const projectTaskOpenProjectView = {
    ...kanbanView,
    Controller: ProjectTaskOpenProjectController,
    buttonTemplates: [...(kanbanView.buttonTemplates || []), "project_view_from_task.KanbanButtons"],
};

registry.category("views").add("project_task_open_project_kanban", projectTaskOpenProjectView);
