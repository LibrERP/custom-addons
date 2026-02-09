# Testing Guide: Core Extended

## Module Overview
The Core Extended module provides an abstract model for row coloring in list views. It allows models that inherit from `row.color` to have configurable color selections for their records.

## Prerequisites
- Module must be installed on the test database (test18)
- Administrator access to Odoo

## Test Cases

### Test 1: Verify Module Installation
**Steps:**
1. Login to Odoo web UI
2. Go to **Apps** menu
3. Search for "Core Extended"
4. Verify the module shows as "Installed"

**Expected Result:** Module status should be "Installed"

---

### Test 2: Verify Cron View Extension
**Steps:**
1. Go to **Settings** → **Technical** → **Automation** → **Scheduled Actions**
2. Open any scheduled action
3. Check if the view loads without errors

**Expected Result:** The scheduled actions form view should load correctly without any errors

---

### Test 3: Test Row Color Inheritance (For Developers)
This module provides an abstract model that other modules can inherit. To test:

**Steps:**
1. Go to **Settings** → **Technical** → **Database Structure** → **Models**
2. Search for "row.color"
3. Verify the model exists with these fields:
   - `color` (Selection field)
   - `row_color` (Char field, computed)

**Expected Result:** The abstract model should be registered with the correct fields

---

### Test 4: Verify Color Selection Options
**Steps:**
1. If you have a model inheriting from `row.color`, open its list view
2. Click on a record to open form view
3. Look for the "Color" field
4. Click on the dropdown to see available colors

**Expected Colors Available:**
- Aqua
- Black
- Blue
- Brown
- Cadet Blue
- Dark Blue
- Fuchsia
- Forest Green
- Green
- Grey
- Red
- Orange

**Expected Result:** All 12 color options should be available in the dropdown

---

## Troubleshooting

### Issue: Module not appearing in Apps
**Solution:** Update the apps list by clicking **Apps** → **Update Apps List**

### Issue: Abstract model not found
**Solution:** This is an abstract model and won't appear in the standard model list unless you enable developer mode and look in the registry.

---

## Notes
- This module is primarily a utility/library module
- Its functionality is best tested through modules that inherit from `row.color`
- The row coloring feature requires proper list view configuration with the `colors` attribute
