# Website Pricelist as Wishlist

## Migration Status

✅ **Ported from Odoo 14 to Odoo 18**

This addon has been successfully migrated from Odoo 14 to Odoo 18 and has passed the initial installation test.

## Description

This module synchronizes products from pricelists to customer wishlists on the website. When a customer is assigned a pricelist with specific products, those products automatically appear in their wishlist on the eCommerce website.

### Features
- Automatic wishlist population from customer pricelists
- Scheduled cron job for daily synchronization
- Support for parent company pricelist inheritance
- Excludes default pricelist to prevent unwanted additions
- Portal users only (excludes backend users)

## Installation

1. Place this addon in your Odoo addons path
2. Ensure Website Sale Wishlist module is installed
3. Update the apps list
4. Install "Website Pricelist as Wishlist" from the Apps menu

## Testing Guide

Please test all features according to the guidelines below:

### Test 1: Verify Module Installation
- Go to **Apps** menu
- Search for "Website Pricelist as Wishlist"
- Verify the module shows as "Installed"

### Test 2: Verify Scheduled Action Created
- Go to **Settings** → **Technical** → **Automation** → **Scheduled Actions**
- Search for "Wishlist Update"
- Verify the cron job exists and is active

### Test 3: Create Test Data
1. Create a product (ensure "Website Published" is checked)
2. Create a pricelist with the product
3. Create a portal user and assign the pricelist

### Test 4: Manually Run Wishlist Update
- Find "Wishlist Update" scheduled action
- Click **Run Manually**
- Verify execution completes without errors

### Test 5: Verify Wishlist Created
- Check product.wishlist records for the test customer
- Products from their pricelist should appear in the wishlist

### Test 6: Test Website Wishlist Display
- Log in as the portal user on the website
- Go to "My Account" → "My Wishlist"
- Verify pricelist products appear

### Test 7: Test Pricelist Change Sync
- Add a new product to the pricelist
- Run the cron manually
- Verify new product appears in wishlist

### Test 8: Test Product Removal
- Remove a product from the pricelist
- Run the cron manually
- Verify product is removed from wishlist

### Test 9: Verify Default Pricelist Excluded
- Assign default pricelist (ID=1) to a customer
- Run the cron
- Verify NO automatic wishlist items created

### Test 10: Verify Non-Portal Users Excluded
- Create a backend user with a pricelist
- Run the cron
- Verify NO wishlist created for this user

## Migration Notes

### Changes Applied During Migration

#### 1. Invalid `numbercall` field on ir.cron
**Error:** `ValueError: Invalid field 'numbercall' on model 'ir.cron'`

The `numbercall` field was removed in Odoo 18. The cron configuration was updated:

```xml
<!-- Before (Odoo 14) -->
<field name="interval_number">1</field>
<field name="interval_type">days</field>
<field name="numbercall">1</field>
<field name="nextcall" eval="(DateTime.now() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')"/>

<!-- After (Odoo 18) -->
<field name="interval_number">1</field>
<field name="interval_type">days</field>
<field name="active">True</field>
```

## ⚠️ Warnings

### Deprecated Field: `product.product.price`
- **Issue:** The `price` field on `product.product` model was deprecated
- **Reference:** https://github.com/odoo/odoo/commit/9e99a9df464d97a74ca320d
- **Impact:** May affect price display functionality. Review and test price-related features.

### Removed Field: `numbercall` in ir.cron
- **Issue:** The `numbercall` field has been removed from `ir.cron` model
- **Reference:** https://github.com/odoo/odoo/commit/2700dd3fd4c45b5282d3803182dfffdfc4418ad8
- **Status:** Fixed during migration

## Technical Notes

### Cron Configuration
- **Interval:** 1 day
- **Model:** product.pricelist
- **Method:** cron_update_wishlist
- **Parameter:** website_id=1 (adjust for multi-website setups)

### Wishlist Behavior
- Creates new wishlist entries for pricelist products
- Updates existing entries when pricelist changes
- Removes entries when products are removed from pricelist
- Skips the default pricelist (ID=1)

## Dependencies

- `base`
- `website_sale_wishlist`
- `product`

## Author

Originally by LibrERP, migrated to Odoo 18.

## License

AGPL-3
