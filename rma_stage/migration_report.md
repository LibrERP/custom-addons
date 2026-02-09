# Migration Report - rma_stage

## Installation Status: ✅ SUCCESS

## Errors Encountered and Fixes Applied

### Error 1: Template-based assets loading deprecated

**Error Message:**
```
ValueError: External ID not found in the system: web.assets_backend
```

**File:** `views/rma_assets.xml`

**Original Code (old template-based approach):**
```xml
<template id="assets_backend" name="rma assets" inherit_id="web.assets_backend">
    <xpath expr="." position="inside">
        <script type="text/javascript" src="/rma_stage/static/src/js/rma_kanban.js"></script>
    </xpath>
</template>
```

**Fix Applied:**
- Removed `views/rma_assets.xml` from manifest data list
- Added `assets` key in `__manifest__.py`:

```python
'assets': {
    'web.assets_backend': [
        'rma_stage/static/src/js/rma_kanban.js',
    ],
},
```

**Explanation:** Starting from Odoo 14, the recommended way to define assets is in the manifest file using the `assets` key rather than using QWeb templates.

---

### Error 2: `attrs` attribute deprecated in views

**Error Message:**
```
ParseError: Since 17.0, the "attrs" and "states" attributes are no longer used.
```

**File:** `wizard/rma_stage_delete_views.xml`

**Original Code:**
```xml
<div attrs="{'invisible': [('rma_count', '>', 0)]}">
<button ... attrs="{'invisible': [('rma_count', '>', 0)]}" />
```

**Fixed Code:**
```xml
<div invisible="rma_count > 0">
<button ... invisible="rma_count > 0" />
```

**Explanation:** In Odoo 17+, the `attrs` dictionary syntax was replaced with direct attribute expressions. The new syntax uses Python-like expressions directly in the `invisible`, `readonly`, and `required` attributes.

---

### Warnings Observed

1. **kanban-box deprecated**: The warning `'kanban-box' is deprecated, define a 'card' template instead` indicates that the kanban views should be updated to use the new card template syntax in Odoo 18.

2. **Missing license key**: Manifest should include `'license': 'AGPL-3',` (already present in this module).

---

## Files Modified

1. `__manifest__.py` - Updated assets loading approach
2. `wizard/rma_stage_delete_views.xml` - Converted attrs syntax to new invisible attribute
3. `static/src/js/rma_kanban.js` - Complete rewrite for Odoo 18 OWL framework
4. `models/rma.py` - Fixed `_read_group_stage_ids` method signature

## Migration Date
February 9, 2026

---

## Post-Installation Testing Errors and Fixes (Updated)

### Error 3: JavaScript "rma_kanban" view not found in registry

**Error Message:**
```
OwlError: The following error occurred in onWillStart: "Cannot find key "rma_kanban" in the "views" registry"
KeyNotFoundError: Cannot find key "rma_kanban" in the "views" registry
```

**Root Cause:**
The JavaScript code in `static/src/js/rma_kanban.js` was using the deprecated Odoo 14/15 widget framework (`odoo.define()`, `web.KanbanController`, `web.view_registry`). Odoo 18 uses the OWL framework with ES6 modules and a different view registry system.

**File:** `static/src/js/rma_kanban.js`

**Original Code (Odoo 14 style):**
```javascript
odoo.define('rma_stage.rma_kanban', function (require) {
'use strict';

var KanbanController = require('web.KanbanController');
var KanbanView = require('web.KanbanView');
var KanbanColumn = require('web.KanbanColumn');
var view_registry = require('web.view_registry');
// ...
view_registry.add('rma_kanban', RmaKanbanView);
});
```

**Fixed Code (Odoo 18 OWL style):**
```javascript
/** @odoo-module **/

import { registry } from "@web/core/registry";
import { kanbanView } from "@web/views/kanban/kanban_view";
import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";
import { KanbanHeader } from "@web/views/kanban/kanban_header";
import { useService } from "@web/core/utils/hooks";

export class RmaKanbanHeader extends KanbanHeader {
    setup() {
        super.setup();
        this.action = useService("action");
    }

    async deleteGroup() {
        const { group } = this.props;
        const resModel = group.groupByField?.relation;
        if (resModel === "rma.stage") {
            const action = await this.orm.call(
                "rma.stage", "unlink_wizard", [[group.value]],
                { context: group.context }
            );
            if (action) {
                this.action.doAction(action, {
                    onClose: async () => {
                        await this.props.list.load();
                        this.props.list.model.notify();
                    }
                });
            }
        } else {
            super.deleteGroup();
        }
    }
}

export class RmaKanbanRenderer extends KanbanRenderer {
    static components = {
        ...KanbanRenderer.components,
        KanbanHeader: RmaKanbanHeader,
    };
}

export const rmaKanbanView = {
    ...kanbanView,
    Renderer: RmaKanbanRenderer,
};

registry.category("views").add("rma_kanban", rmaKanbanView);
```

**Explanation:** 
- Odoo 18 uses ES6 modules with `import`/`export` instead of AMD-style `odoo.define()`
- Views are registered using `registry.category("views").add()` instead of `view_registry.add()`
- Controller/Renderer classes extend OWL-based components from `@web/views/kanban/`
- Services like `orm` and `action` are accessed using `useService()` hook

---

### Error 4: `_read_group_stage_ids()` missing 'order' argument

**Error Message:**
```
TypeError: Rma._read_group_stage_ids() missing 1 required positional argument: 'order'
```

**Root Cause:**
In Odoo 18, the `group_expand` method signature changed from 4 parameters `(self, stages, domain, order)` to 3 parameters `(self, groups, domain)`.

**File:** `models/rma.py`

**Original Code:**
```python
@api.model
def _read_group_stage_ids(self, stages, domain, order):
    search_domain = []
    stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
    return stages.browse(stage_ids)
```

**Fixed Code:**
```python
@api.model
def _read_group_stage_ids(self, stages, domain):
    """ Read group customization to show all stages even when empty.
    
    Note: In Odoo 18, the group_expand method signature changed to 
    (self, groups, domain) instead of the old (self, stages, domain, order).
    """
    search_domain = []
    return self.env['rma.stage'].search(search_domain)
```

**Explanation:**
- The `order` parameter was removed in Odoo 18's `group_expand` function
- The method should now use `self.env['rma.stage'].search()` directly instead of using `stages._search()` with access_rights_uid

---

## Summary of All Changes

| File | Change Type | Description |
|------|-------------|-------------|
| `__manifest__.py` | Modified | Added `assets` key for JS loading |
| `wizard/rma_stage_delete_views.xml` | Modified | Converted `attrs` to direct `invisible` attribute |
| `static/src/js/rma_kanban.js` | **Rewritten** | Complete rewrite for Odoo 18 OWL framework |
| `models/rma.py` | Modified | Fixed `_read_group_stage_ids` method signature |

## Testing Status

After applying all fixes:
- ✅ Module installs without errors
- ✅ Odoo server starts successfully
- ✅ No JavaScript registry errors
- ✅ RMA Kanban view loads correctly
- ✅ Stage grouping works properly
