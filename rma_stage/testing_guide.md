# Testing Guide: RMA Stage

## Module Overview
This module adds configurable stages (like a Kanban workflow) to the RMA (Return Merchandise Authorization) module. It enables tracking RMA progress through customizable stages with features like folding, closing stages, and stage transitions.

## Prerequisites
- Module must be installed on the test database (test18)
- Base RMA module must be installed
- Administrator access to Odoo
- Developer mode enabled for some tests

## Test Cases

### Test 1: Verify Module Installation
**Steps:**
1. Login to Odoo web UI
2. Go to **Apps** menu
3. Search for "RMA Stage"
4. Verify the module shows as "Installed"

**Expected Result:** Module status should be "Installed"

---

### Test 2: Access RMA Stages Configuration
**Steps:**
1. Go to **RMA** menu (or Inventory → Operations → RMA, depending on your setup)
2. Look for **Configuration** → **Stages** menu
3. Click on it

**Expected Result:** A list view of RMA stages should appear

---

### Test 3: Create a New RMA Stage
**Steps:**
1. Go to RMA → Configuration → Stages
2. Click **New**
3. Fill in the following:
   - **Stage Name:** "Under Review"
   - **Sequence:** 10
   - **Folded in Kanban:** Unchecked
   - **Closing Stage:** Unchecked
4. Click **Save**

**Expected Result:** New stage should be created and visible in the stages list

---

### Test 4: Create a Closing Stage
**Steps:**
1. Go to RMA → Configuration → Stages
2. Click **New**
3. Fill in:
   - **Stage Name:** "Completed"
   - **Sequence:** 100
   - **Closing Stage:** Checked ✓
   - **Folded in Kanban:** Checked ✓
4. Click **Save**

**Expected Result:** A closing stage should be created that will be folded by default in Kanban view

---

### Test 5: Configure Next Stages
**Steps:**
1. Open an existing stage (e.g., "Under Review")
2. Look for "Next Stages" field
3. Add one or more stages that can follow this stage
4. Save

**Expected Result:** The stage transitions should be saved, defining the workflow path

---

### Test 6: View RMA in Kanban View
**Steps:**
1. Go to RMA list
2. Switch to **Kanban View** (using the view switcher icon)
3. Observe the stages displayed as columns

**Expected Result:** 
- Stages should appear as Kanban columns
- Folded stages should be collapsed
- RMA records should be organized by their stage

---

### Test 7: Create an RMA and Assign Stage
**Steps:**
1. Go to RMA → Create (or New RMA)
2. Fill in required fields (partner, product, etc.)
3. Observe the **Stage** field - it should have a default value
4. Try changing the stage using the dropdown
5. Save the RMA

**Expected Result:** 
- Default stage should be automatically assigned
- Stage can be changed from the dropdown
- RMA record appears in the correct Kanban column

---

### Test 8: Drag and Drop in Kanban
**Steps:**
1. Go to RMA Kanban view
2. Find an RMA card in one stage
3. Drag it to a different stage column
4. Release (drop) the card

**Expected Result:** 
- RMA should move to the new stage
- The stage_id field should be updated automatically

---

### Test 9: Test Kanban State
**Steps:**
1. Open an RMA record in form view
2. Look for the **Kanban State** field
3. Try changing it between:
   - Normal (In Progress) - Grey
   - Done (Ready) - Green
   - Blocked - Red
4. Save and check Kanban view

**Expected Result:** The Kanban state indicator should change color accordingly

---

### Test 10: Test Priority Field
**Steps:**
1. Open an RMA record
2. Look for the **Priority** field (usually shown as stars)
3. Toggle between Normal and Important
4. Save

**Expected Result:** Priority should be saved and may affect the visual display of the RMA card

---

### Test 11: Delete Stage with Wizard
**Steps:**
1. Go to RMA → Configuration → Stages
2. Select a stage that has RMA records in it
3. Click **Delete** (or Action → Delete)
4. A wizard should appear asking what to do with existing RMAs

**Expected Result:** 
- Delete wizard should appear
- Options to move RMAs to another stage or cancel should be provided

---

### Test 12: Test Stage Folding
**Steps:**
1. Create or edit a stage
2. Check "Folded in Kanban"
3. Save
4. Go to RMA Kanban view
5. Look for the stage column

**Expected Result:** 
- Stage should appear collapsed/folded
- Can be expanded by clicking on it

---

## Troubleshooting

### Issue: Stages not appearing in Kanban
**Solution:** 
1. Ensure at least one stage exists
2. Check that stages are not all set to "Folded"
3. Verify the stage has no restricting filters

### Issue: Cannot drag RMA between stages
**Solution:** 
1. Check user permissions
2. Verify JavaScript is loading correctly (check browser console)
3. Clear browser cache

### Issue: Default stage not being assigned
**Solution:** 
1. Ensure at least one stage exists with `fold=False` and `is_closed=False`
2. Check the sequence - lowest sequence unfold non-closed stage is the default

---

## Notes
- Stages are shared across all RMA teams unless team filtering is applied
- Closing stages mark RMAs as completed/closed
- The Kanban JavaScript file enhances the drag-drop functionality
