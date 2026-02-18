# RMA Supplier

## Migration Status

✅ **Ported from Odoo 14 to Odoo 18**

This addon has been successfully migrated from Odoo 14 to Odoo 18 and has passed the initial installation test.

**No code modifications were required** - the addon was already compatible with Odoo 18.

## Description

This module extends the RMA (Return Merchandise Authorization) module by adding supplier-related fields. It allows tracking of supplier information, goods arrival dates, return documents, credit notes, and transportation documents for RMA cases.

### Features
- Supplier (Fornitore) field on RMA
- Inventory State (Stato Magazzino) tracking
- Goods Arrival Date (Data Arrivo Merce)
- Return Document (Documento di Reso) reference
- Supplier Credit Note (Nota Accredito Fornitore) tracking
- Supplier Transportation Document (DDT Fornitore)

## Installation

1. Place this addon in your Odoo addons path
2. Ensure the base `rma` module is installed
3. Update the apps list
4. Install "RMA Supplier" from the Apps menu

## Testing Guide

Please test all features according to the guidelines below:

### Test 1: Verify Module Installation
- Go to **Apps** menu
- Search for "RMA Supplier"
- Verify the module shows as "Installed"

### Test 2: Verify New Fields on RMA Form
- Open an RMA record
- Verify the following fields are visible:
  - Fornitore (Supplier)
  - Stato Magazzino (Inventory State)
  - Data Arrivo Merce (Goods Arrival Date)
  - Documento di Reso (Return Document)
  - Nota Accredito Fornitore (Supplier Credit Note)
  - DDT Fornitore (Supplier Transportation Document)

### Test 3: Create RMA with Supplier Information
- Create a new RMA
- Fill in all supplier-specific fields
- Save and verify data is persisted

### Test 4: Test Inventory State Selection
- Open an RMA record
- Click on "Stato Magazzino" dropdown
- Select a state and save

### Test 5: Configure Inventory States
- Look for RMA → Configuration → Inventory States
- Create a new inventory state
- Verify it appears in the RMA form dropdown

### Test 6: Filter RMA by Supplier
- Go to RMA list view
- Group by "Fornitore" (Supplier)
- Verify filtering works correctly

### Test 7: Search RMA by Document Numbers
- Search for a specific document number
- Verify matching RMAs appear in results

### Test 8: Verify Data Integrity
- Create an RMA with all supplier fields filled
- Close and reopen the record
- Verify all data is correctly preserved

## Migration Notes

No code modifications were required for this addon. It was already compatible with Odoo 18.

## Technical Notes

- This module uses Italian field labels (Fornitore, DDT, etc.)
- All supplier fields are optional
- The inventory state model (`rma.inventory.state`) is separate and can be configured independently
- Integration with purchase orders or supplier returns may require additional modules

## Dependencies

- `base`
- `rma`

## Author

Originally by LibrERP, migrated to Odoo 18.

## License

AGPL-3
