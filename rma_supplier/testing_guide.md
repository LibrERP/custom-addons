# Testing Guide: RMA Supplier

## Module Overview
This module extends the RMA (Return Merchandise Authorization) module by adding supplier-related fields. It allows tracking of supplier information, goods arrival dates, return documents, credit notes, and transportation documents for RMA cases.

## Prerequisites
- Module must be installed on the test database (test18)
- Base RMA module must be installed
- Administrator access to Odoo
- At least one supplier (vendor) partner created

## Test Cases

### Test 1: Verify Module Installation
**Steps:**
1. Login to Odoo web UI
2. Go to **Apps** menu
3. Search for "RMA Supplier"
4. Verify the module shows as "Installed"

**Expected Result:** Module status should be "Installed"

---

### Test 2: Verify New Fields on RMA Form
**Steps:**
1. Go to RMA menu
2. Open an existing RMA record or create a new one
3. Look for the following new fields in the form view:

**Expected Fields:**
- **Fornitore (Supplier):** Many2one field to select a partner/supplier
- **Stato Magazzino (Inventory State):** Selection field for inventory status
- **Data Arrivo Merce (Goods Arrival Date):** Date field
- **Documento di Reso (Return Document):** Text field
- **Nota Accredito Fornitore (Supplier Credit Note):** Text field
- **DDT Fornitore (Supplier Transportation Document):** Text field

**Expected Result:** All six new fields should be visible on the RMA form

---

### Test 3: Create RMA with Supplier Information
**Steps:**
1. Go to RMA → Create New RMA
2. Fill in standard RMA fields (partner, product, reason)
3. Fill in supplier-specific fields:
   - **Fornitore:** Select a vendor from the list
   - **Data Arrivo Merce:** Select a date
   - **Documento di Reso:** Enter "RET-2024-001"
   - **Nota Accredito Fornitore:** Enter "CN-2024-001"
   - **DDT Fornitore:** Enter "DDT-2024-001"
4. Save the RMA

**Expected Result:** All supplier information should be saved correctly

---

### Test 4: Test Inventory State Selection
**Steps:**
1. Open an RMA record
2. Look for the "Stato Magazzino" field
3. Click on the dropdown
4. View available inventory states
5. Select one and save

**Expected Result:** 
- Dropdown should show available inventory states
- Selected state should be saved

---

### Test 5: Configure Inventory States
**Steps:**
1. Go to **Settings** → **Technical** → **Database Structure** → **Models**
2. Search for "rma.inventory.state"
3. Or look for a menu under RMA → Configuration → Inventory States
4. Create a new inventory state:
   - **Name:** "In Warehouse"
5. Save

**Expected Result:** New inventory state should be available in the RMA form dropdown

---

### Test 6: Filter RMA by Supplier
**Steps:**
1. Go to RMA list view
2. Use the search bar
3. Add a filter or group by "Fornitore" (Supplier)
4. Select a specific supplier

**Expected Result:** RMA list should filter to show only RMAs for the selected supplier

---

### Test 7: Search RMA by Document Numbers
**Steps:**
1. Go to RMA list view
2. Use the search bar
3. Search for a specific document number (e.g., "RET-2024-001")

**Expected Result:** RMAs with matching document numbers should appear in search results

---

### Test 8: Verify Data Integrity
**Steps:**
1. Create an RMA with all supplier fields filled
2. Save and close the form
3. Reopen the same RMA record
4. Verify all supplier information is correctly preserved

**Expected Result:** All entered data should be accurately saved and displayed

---

### Test 9: Test Required Fields Behavior
**Steps:**
1. Create a new RMA
2. Try to save without filling supplier fields
3. Observe if any validation errors occur

**Expected Result:** 
- Supplier fields should NOT be required (based on field definition)
- RMA should save successfully even without supplier information

---

### Test 10: Test Supplier Selection from Vendors
**Steps:**
1. Create or open an RMA
2. Click on the "Fornitore" field
3. Search for a vendor/supplier
4. Note: Only vendors should ideally be shown, but the field may show all partners

**Expected Result:** 
- Partner selection should work
- Selected supplier should be saved with the RMA

---

### Test 11: Export RMA with Supplier Data
**Steps:**
1. Go to RMA list view
2. Select multiple RMA records
3. Use Action → Export
4. Include supplier-related fields in the export
5. Export to Excel/CSV

**Expected Result:** 
- Export should include supplier fields
- Data should be correctly formatted

---

### Test 12: Print/Report with Supplier Information
**Steps:**
1. Open an RMA with supplier information
2. Click Print (if a report template exists)
3. Check if supplier information appears on the printed document

**Expected Result:** Supplier information should be included in RMA reports (if report is configured)

---

## Troubleshooting

### Issue: Supplier fields not visible
**Solution:** 
1. Check if the view was properly updated
2. Clear browser cache
3. Restart Odoo server and try again
4. Check if you have proper access rights

### Issue: Inventory State dropdown is empty
**Solution:** 
1. Go to configuration and create inventory states
2. Check `data/inventory_state.xml` for pre-configured states
3. Try updating the module

### Issue: Cannot select supplier
**Solution:** 
1. Ensure vendors/suppliers exist in the system
2. Create a new contact with "Is a Company" checked
3. Check if there are domain filters on the field

---

## Notes
- This module uses Italian field labels (Fornitore, DDT, etc.)
- All supplier fields are optional
- The inventory state model is separate and can be configured independently
- Integration with purchase orders or supplier returns may require additional modules
