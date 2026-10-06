# Generate Missing Reordering Rules

A wizard that creates reordering rules (min/max) for all storable products that do not have one yet.

## What it does

- **Bulk creation** - A rule for every storable product that has none, in one step.
- **You choose where** - Pick the warehouse and the location the rules apply to.
- **Your own limits** - Set the minimum and maximum quantity for the new rules (0 / 0 by default).
- **Category filter** - Optionally limit the run to one product category and its subcategories.
- **Nothing overwritten** - Products that already have a rule are skipped. See the count before you generate.
- **Review the result** - After generating you land on the list of the new rules, ready to adjust.

## How to use it

1. Open Inventory > Operations > Generate Missing Reordering Rules (needs the Inventory Administrator role).
2. Choose the Warehouse. The Location defaults to its stock location; change it if needed.
3. Optionally pick a Product Category, and set the Minimum and Maximum Quantity for the new rules.
4. Choose which products to skip: those that have a rule in any location (default), or only those with a rule in the chosen location.
5. Check Products to Receive a Rule - it shows how many rules will be created - and press Generate.
6. The new rules open in a list. Adjust min/max per product there, or use Inventory > Operations > Replenishment.

## Good to know

- Only storable products are considered (Track Inventory ticked).
- Rules are created with the standard trigger of Odoo (automatic).
- Archived rules count as existing rules, so a product whose rule you archived is not given a new one.
- Running it again is safe: it only adds rules for products that still have none.

## Technical

- Transient model `stock.orderpoint.generator` (`models/orderpoint_generator.py`), form + menu in `views/orderpoint_generator_views.xml`.
- Rules are created through the standard `stock.warehouse.orderpoint` model, in one `create` call.
- Depends on: `stock`.

## Status

Source: client module (Odoo 19), where the rule was created by a hand-run scheduled action in a hard-coded location. Rewritten as a wizard. Odoo 20 build.
