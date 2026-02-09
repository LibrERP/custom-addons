# Migration Report: website_pricelist_as_wishlist

## Summary
- **Status**: ✅ Successfully Installed
- **Target Database**: test18
- **Odoo Version**: 18.0

## Installation Details
- Module loaded in 0.24s, 51 queries
- Registry loaded in 5.771s

## Issues Encountered & Fixes Applied

### Issue 1: Invalid `numbercall` field on ir.cron model
- **Error**: `ValueError: Invalid field 'numbercall' on model 'ir.cron'`
- **File**: `data/ir_cron_data.xml`
- **Cause**: The `numbercall` field was renamed in Odoo 18. Additionally, the `nextcall` field with eval expression is not needed for standard cron jobs.
- **Solution**: Removed `numbercall` and `nextcall` fields, replaced with `active` field.

#### Before:
```xml
<field name="user_id" ref="base.user_root"/>
<field name="interval_number">1</field>
<field name="interval_type">days</field>
<field name="numbercall">1</field>
<field name="nextcall" eval="(DateTime.now() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')"/>
```

#### After:
```xml
<field name="user_id" ref="base.user_root"/>
<field name="interval_number">1</field>
<field name="interval_type">days</field>
<field name="active">True</field>
```

## Warnings (non-blocking)
The following warnings appeared during installation but are from other addons in the system:

1. **Precompute warnings** (from crm module):
   - `Field crm.lead.team_id cannot be precomputed`
   - `Field crm.lead.lead_properties cannot be precomputed`

These warnings are informational and do not affect the addon functionality.

## Migration Notes

### Odoo 18 ir.cron Changes
- The `numbercall` field has been deprecated/removed in Odoo 18
- For crons that should run indefinitely, simply omit the field or use `active` to enable/disable
- The `nextcall` field is automatically computed by Odoo based on `interval_number` and `interval_type`

## Migration Date
2025-02-09

## Conclusion
The website_pricelist_as_wishlist addon required one change to the ir.cron data file to be compatible with Odoo 18.
