# Stock Move Import

This module adds an "Import Moves" button on the Transfer form (stock.picking). The button opens Odoo's built-in import wizard for `stock.move` so you can upload a CSV or XLSX file.

## What the sample CSV contains

`tests/sample_import_moves.csv` uses these columns:

- `Product`: Product name (or internal reference + name) that exists in your database.
- `Quantity`: Quantity for the move.

## How to import

1. Open a transfer that is not done or cancelled.
2. Click **Import Moves** in the header.
3. Upload the CSV/XLSX file.
4. Map columns to fields if needed.
5. Click **Test** to validate, then **Import**.

Notes:
- Products must already exist in the database.
- The import uses the current picking as the target, so you do not need a Picking column in the file.

## Files

- `models/stock_picking.py`: Opens the standard import wizard for stock moves.
- `views/stock_picking_views.xml`: Adds the Import Moves button.
- `tests/sample_import_moves.csv`: Sample import file.
