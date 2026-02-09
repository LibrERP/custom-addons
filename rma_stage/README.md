# RMA Stage

## Migration Status

✅ **Ported from Odoo 14 to Odoo 18**

This addon has been successfully migrated from Odoo 14 to Odoo 18 and has passed the initial installation test.

## Description

This module adds configurable stages (like a Kanban workflow) to the RMA (Return Merchandise Authorization) module. It enables tracking RMA progress through customizable stages with features like folding, closing stages, and stage transitions.

### Features
- Configurable RMA stages with sequence ordering
- Kanban view for RMA with stage columns
- Stage folding in Kanban view
- Closing stages for completed RMAs
- Next stage configuration for workflow control
- Custom delete wizard for stages with existing RMAs
- Team-based stage filtering

## Installation

1. Place this addon in your Odoo addons path
2. Ensure the base `rma` module is installed
3. Update the apps list
4. Install "RMA Stage" from the Apps menu

## Testing Guide

Please test all features according to the guidelines below:

### Test 1: Verify Module Installation
- Go to **Apps** menu
- Search for "RMA Stage"
- Verify the module shows as "Installed"

### Test 2: Access RMA Stages Configuration
- Go to **RMA** → **Configuration** → **Stages**
- Verify the stages list view appears

### Test 3: Create a New RMA Stage
- Go to RMA → Configuration → Stages → **New**
- Fill in: Stage Name, Sequence, Folded in Kanban, Closing Stage
- Save and verify the stage is created

### Test 4: Configure Next Stages
- Open an existing stage
- Add stages to the "Next Stages" field
- Save and verify workflow transitions

### Test 5: View RMA in Kanban View
- Go to RMA list
- Switch to Kanban View
- Verify stages appear as columns
- Verify RMAs are organized by stage

### Test 6: Drag and Drop in Kanban
- Drag an RMA card to a different stage
- Verify the stage_id is updated

### Test 7: Test Delete Stage with Wizard
- Try to delete a stage that has RMA records
- Verify the delete wizard appears with options to move RMAs

### Test 8: Test Stage Folding
- Set a stage as "Folded in Kanban"
- Verify it appears collapsed in Kanban view

## Migration Notes

### Changes Applied During Migration

#### 1. Template-based assets loading deprecated
**Error:** `ValueError: External ID not found in the system: web.assets_backend`

Changed from QWeb template to manifest `assets` key:

```python
# In __manifest__.py
'assets': {
    'web.assets_backend': [
        'rma_stage/static/src/js/rma_kanban.js',
    ],
},
```

#### 2. `attrs` attribute deprecated in views
**Error:** `ParseError: Since 17.0, the "attrs" and "states" attributes are no longer used`

```xml
<!-- Before -->
<div attrs="{'invisible': [('rma_count', '>', 0)]}">

<!-- After -->
<div invisible="rma_count > 0">
```

#### 3. JavaScript complete rewrite for OWL framework
**Error:** `KeyNotFoundError: Cannot find key "rma_kanban" in the "views" registry`

The JavaScript was completely rewritten from Odoo 14 widget framework to Odoo 18 OWL framework:

```javascript
// Before (Odoo 14)
odoo.define('rma_stage.rma_kanban', function (require) {
    var KanbanController = require('web.KanbanController');
    var view_registry = require('web.view_registry');
    view_registry.add('rma_kanban', RmaKanbanView);
});

// After (Odoo 18)
import { registry } from "@web/core/registry";
import { kanbanView } from "@web/views/kanban/kanban_view";
import { KanbanHeader } from "@web/views/kanban/kanban_header";

export class RmaKanbanHeader extends KanbanHeader {
    async deleteGroup() {
        // Custom delete logic with wizard
    }
}

registry.category("views").add("rma_kanban", rmaKanbanView);
```

#### 4. `_read_group_stage_ids()` signature changed
**Error:** `TypeError: Rma._read_group_stage_ids() missing 1 required positional argument: 'order'`

In Odoo 18, the `group_expand` method signature changed from 4 to 3 parameters:

```python
# Before (Odoo 14)
def _read_group_stage_ids(self, stages, domain, order):
    stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
    return stages.browse(stage_ids)

# After (Odoo 18)
def _read_group_stage_ids(self, stages, domain):
    return self.env['rma.stage'].search(search_domain)
```

## ⚠️ Warnings

### Kanban Template Deprecation
The warning `'kanban-box' is deprecated, define a 'card' template instead` indicates that the kanban views should be updated to use the new card template syntax in Odoo 18. This is non-blocking but should be addressed in future updates.

## Dependencies

- `base`
- `web`
- `rma`

## Author

Originally by Codebeex srl (www.codebeex.com), migrated to Odoo 18.

## License

AGPL-3
