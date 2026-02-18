# Core Extended

## Migration Status

✅ **Ported from Odoo 14 to Odoo 18**

This addon has been successfully migrated from Odoo 14 to Odoo 18 and has passed the initial installation test.

## Description

The Core Extended module provides an abstract model for row coloring in list views. It allows models that inherit from `row.color` to have configurable color selections for their records.

### Features
- Abstract `row.color` model for inheritance
- 12 predefined color options (Aqua, Black, Blue, Brown, Cadet Blue, Dark Blue, Fuchsia, Forest Green, Green, Grey, Red, Orange)
- Computed `row_color` field for list view styling

## Installation

1. Place this addon in your Odoo addons path
2. Update the apps list
3. Install "Core Extended" from the Apps menu

## Testing Guide

Please test all features according to the guidelines below:

### Test 1: Verify Module Installation
- Go to **Apps** menu
- Search for "Core Extended"
- Verify the module shows as "Installed"

### Test 2: Verify Cron View Extension
- Go to **Settings** → **Technical** → **Automation** → **Scheduled Actions**
- Open any scheduled action
- Check if the view loads without errors

### Test 3: Test Row Color Inheritance
- Go to **Settings** → **Technical** → **Database Structure** → **Models**
- Search for "row.color"
- Verify the model exists with `color` and `row_color` fields

### Test 4: Verify Color Selection Options
If you have a model inheriting from `row.color`:
- Open a record in form view
- Check the "Color" field dropdown
- Verify all 12 color options are available

## Migration Notes

### Changes Applied During Migration

#### 1. `@api.one` decorator removed
**Error:** `AttributeError: module 'odoo.api' has no attribute 'one'`

The `@api.one` decorator was deprecated since Odoo 10 and removed in Odoo 18. Methods now iterate over records manually.

```python
# Before (Odoo 14)
@api.one
@api.depends('color')
def _get_color(self):
    self.row_color = self.color

# After (Odoo 18)
@api.depends('color')
def _get_color(self):
    for record in self:
        record.row_color = record.color
```

#### 2. Translation function at module level
The `_()` translation function should not be used at module level. Selection field strings are automatically translated.

```python
# Before
COLOR_SELECTION = [('aqua', _(u"Aqua")), ...]

# After
COLOR_SELECTION = [('aqua', "Aqua"), ...]
```

#### 3. Deprecated `select=True` parameter
The `select=True` parameter was replaced by `index=True`.

```python
# Before
color = fields.Selection(COLOR_SELECTION, _('Color'), select=True, default='black')

# After
color = fields.Selection(COLOR_SELECTION, string='Color', index=True, default='black')
```

## Dependencies

- `base`

## Author

Originally by LibrERP, migrated to Odoo 18.

## License

AGPL-3
