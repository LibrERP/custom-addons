# Migration Report - core_extended

## Installation Status: ✅ SUCCESS

## Errors Encountered and Fixes Applied

### Error 1: `@api.one` decorator removed in Odoo 18

**Error Message:**
```
AttributeError: module 'odoo.api' has no attribute 'one'
```

**File:** `color.py`, line 52

**Original Code:**
```python
@api.one
@api.depends('color')
def _get_color(self):
    self.row_color = self.color
```

**Fixed Code:**
```python
@api.depends('color')
def _get_color(self):
    for record in self:
        record.row_color = record.color
```

**Explanation:** The `@api.one` decorator has been deprecated since Odoo 10 and completely removed in Odoo 18. Methods must now iterate over records manually.

---

### Error 2: Using `_()` translation function at module level

**Error Message:**
```
WARNING odoo.tools.translate: no translation language detected, skipping translation
```

**File:** `color.py`, lines 23-36

**Original Code:**
```python
from odoo import models, fields, api, _

COLOR_SELECTION = [
    ('aqua', _(u"Aqua")),
    ('black', _(u"Black")),
    ...
]
```

**Fixed Code:**
```python
from odoo import models, fields, api

COLOR_SELECTION = [
    ('aqua', "Aqua"),
    ('black', "Black"),
    ...
]
```

**Explanation:** The `_()` translation function should not be used at module level (outside methods). Translation strings in selection fields are automatically translated when defined as plain strings.

---

### Error 3: Deprecated `select=True` parameter

**File:** `color.py`, line 49

**Original Code:**
```python
color = fields.Selection(COLOR_SELECTION, _('Color'), select=True, default='black')
```

**Fixed Code:**
```python
color = fields.Selection(COLOR_SELECTION, string='Color', index=True, default='black')
```

**Explanation:** The `select=True` parameter has been replaced by `index=True` in modern Odoo versions. Also, field labels should use `string=` parameter instead of positional `_()` calls.

---

## Migration Date
February 9, 2026
