# Testing Guide: Website Pricelist as Wishlist

## Module Overview
This module synchronizes products from pricelists to customer wishlists on the website. When a customer is assigned a pricelist with specific products, those products automatically appear in their wishlist on the eCommerce website.

## Prerequisites
- Module must be installed on the test database (test18)
- Website Sale Wishlist module must be installed
- eCommerce (Website Sale) module configured
- At least one active website
- Portal users/customers created
- Products and pricelists configured

## Test Cases

### Test 1: Verify Module Installation
**Steps:**
1. Login to Odoo web UI
2. Go to **Apps** menu
3. Search for "Website Pricelist as Wishlist"
4. Verify the module shows as "Installed"

**Expected Result:** Module status should be "Installed"

---

### Test 2: Verify Scheduled Action Created
**Steps:**
1. Go to **Settings** → **Technical** → **Automation** → **Scheduled Actions**
2. Search for "Wishlist" or look for the cron job created by this module
3. Open the scheduled action

**Expected Result:** 
- A scheduled action named "Wishlist Update" (or similar) should exist
- It should be active
- Interval should be set to 1 day

---

### Test 3: Create Test Data Setup
**Steps:**
1. **Create a Product:**
   - Go to Sales → Products → Create
   - Name: "Test Product for Wishlist"
   - Ensure "Website Published" is checked
   - Save

2. **Create a Pricelist with Product:**
   - Go to Sales → Pricelists → Create
   - Name: "VIP Customer Pricelist"
   - Add a pricelist item with the test product
   - Save

3. **Create a Portal User:**
   - Go to Contacts → Create
   - Name: "Test Customer"
   - Email: "testcustomer@example.com"
   - Click "Grant portal access"
   - Go to Sales tab and assign the VIP pricelist

**Expected Result:** Test data should be created successfully

---

### Test 4: Manually Run Wishlist Update
**Steps:**
1. Go to **Settings** → **Technical** → **Automation** → **Scheduled Actions**
2. Find "Wishlist Update" scheduled action
3. Click **Run Manually** button
4. Wait for execution to complete

**Expected Result:** The cron job should execute without errors

---

### Test 5: Verify Wishlist Created for Portal User
**Steps:**
1. Go to **Settings** → **Technical** → **Database Structure** → **Models**
2. Search for "product.wishlist" and view records
3. Or use developer mode to access wishlist records directly
4. Filter by the test customer partner

**Expected Result:** 
- Wishlist records should exist for the test customer
- Products from their pricelist should appear in the wishlist

---

### Test 6: Test Website Wishlist Display
**Steps:**
1. Open an incognito/private browser window
2. Navigate to your Odoo website (e.g., http://localhost:8069)
3. Log in as the portal user (testcustomer@example.com)
4. Go to "My Account" → "My Wishlist" (or click wishlist icon)
5. View the wishlist products

**Expected Result:** 
- Products from the customer's pricelist should appear in the wishlist
- Products should be displayed with correct pricing

---

### Test 7: Test Pricelist Change Sync
**Steps:**
1. Add a new product to the VIP pricelist:
   - Go to Sales → Pricelists → VIP Customer Pricelist
   - Add another product item
   - Save
2. Run the wishlist update cron manually
3. Check the customer's wishlist (either in backend or website)

**Expected Result:** 
- New product should appear in the customer's wishlist
- Existing wishlist items should remain

---

### Test 8: Test Product Removal from Pricelist
**Steps:**
1. Remove a product from the VIP pricelist:
   - Go to Sales → Pricelists → VIP Customer Pricelist
   - Delete one of the product items
   - Save
2. Run the wishlist update cron manually
3. Check the customer's wishlist

**Expected Result:** 
- Removed product should no longer appear in the wishlist
- Other products should remain

---

### Test 9: Test Multiple Customers Same Pricelist
**Steps:**
1. Create another portal user with the same VIP pricelist
2. Run the wishlist update cron
3. Check wishlists for both customers

**Expected Result:** 
- Both customers should have the same products in their wishlists
- Each customer's wishlist should be independent

---

### Test 10: Test Parent Company Pricelist
**Steps:**
1. Create a parent company contact with the VIP pricelist
2. Create a child contact under this company
3. Grant portal access to the child contact
4. Run the wishlist update cron
5. Check the child contact's wishlist

**Expected Result:** 
- Child contacts should inherit pricelist from parent
- Wishlist should be populated based on parent's pricelist

---

### Test 11: Verify Cron Excludes Default Pricelist
**Steps:**
1. Check that the default pricelist (ID=1) is excluded
2. Assign default pricelist to a customer
3. Run the cron
4. Check if wishlist was created

**Expected Result:** 
- Customers with only the default pricelist (ID=1) should NOT get automatic wishlist items
- This is by design to prevent adding all products to everyone's wishlist

---

### Test 12: Test Non-Portal Users Excluded
**Steps:**
1. Create a regular backend user (not portal)
2. Assign them a pricelist with products
3. Run the wishlist update cron
4. Check if wishlist was created for this user

**Expected Result:** 
- Only portal users should get wishlist items
- Backend/internal users should be excluded

---

### Test 13: Performance Test (Large Data)
**Steps:**
1. Create multiple pricelists with many products
2. Create several portal users with different pricelists
3. Run the cron
4. Monitor execution time and system resources

**Expected Result:** 
- Cron should complete without timeout
- System should remain responsive

---

## Troubleshooting

### Issue: Wishlist not updating
**Solution:** 
1. Check if the cron job is active
2. Run the cron manually
3. Check Odoo logs for errors
4. Verify the customer has portal access

### Issue: Products not appearing on website wishlist
**Solution:** 
1. Ensure products are published on website
2. Check if product has variants (only variant products work)
3. Clear browser cache
4. Log out and log back in as portal user

### Issue: Cron job errors
**Solution:** 
1. Check Odoo server logs
2. Verify website_id parameter (default is 1)
3. Ensure product.wishlist model is accessible

### Issue: All customers getting same wishlist
**Solution:** 
1. Check pricelist assignments on customer records
2. Verify the `pricelist_ids` field exists on partner
3. Check the filter logic in the code

---

## Technical Notes

### Cron Configuration
- **Interval:** 1 day
- **Model:** product.pricelist
- **Method:** cron_update_wishlist
- **Parameter:** website_id=1 (adjust for multi-website setups)

### Field Dependencies
- Partner must have `pricelist_ids` many2many field
- Or inherit pricelist from parent company
- Portal group membership is required

### Wishlist Behavior
- Creates new wishlist entries for pricelist products
- Updates existing entries when pricelist changes
- Removes entries when products are removed from pricelist
- Skips the default pricelist (ID=1)

---

## Notes
- This module works with the website wishlist feature
- Useful for B2B scenarios where specific customers see specific products
- The website_id parameter should match your active website
- Multi-website setups may need customization
