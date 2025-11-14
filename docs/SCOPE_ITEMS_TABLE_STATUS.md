# scope_items Table Status

## Current Structure (Found via API)

✅ **Existing Columns:**
- `id` (UUID, Primary Key)
- `subcontract_id` (UUID, Foreign Key)
- `category` (TEXT)
- `description` (TEXT)
- `created_at` (TIMESTAMP)

## Missing Columns (Need to Add)

❌ **Missing Columns Needed for Your Vision:**

1. **`subcategory`** - For Level 2 breakdown (e.g., "Outlets", "Conduit")
2. **`component`** - For Level 3 breakdown (e.g., "GFCI Outlets") - optional
3. **`quantity`** - How many units (e.g., 25, 500, 1)
4. **`unit`** - Unit of measure (EA, SF, LF, HR, etc.)
5. **`unit_price`** - Price per unit (for historical cost tracking)
6. **`line_total`** - Total for this line item (quantity × unit_price)
7. **`is_included`** - TRUE = included, FALSE = excluded
8. **`breakdown_level`** - 1, 2, or 3 (for AI consolidation logic)
9. **`display_order`** - Order for HTML generation
10. **`updated_at`** - Track when items are modified

## Migration Script Created

✅ **Migration file:** `backend/migrations/002_enhance_scope_items.sql`

This script will:
- Add all missing columns
- Create indexes for performance
- Add auto-update trigger for `updated_at`
- Add helpful comments explaining each column

## Next Steps

1. **Run the migration** in Supabase SQL Editor:
   - Open Supabase Dashboard → SQL Editor
   - Copy/paste contents of `backend/migrations/002_enhance_scope_items.sql`
   - Run it

2. **After migration:**
   - `scope_items` table will be fully flexible
   - Can handle unlimited scope items
   - Supports your consolidation logic
   - Ready for AI processing

## Example After Migration

**Proposal has:**
- Electrical > Outlets > GFCI: 10 EA @ $45 = $450
- Electrical > Outlets > Standard: 15 EA @ $35 = $525
- Electrical > Conduit: 500 LF @ $8 = $4,000
- **Excluded:** Demolition work

**Stored as rows:**

| id | subcontract_id | category | subcategory | component | description | quantity | unit | unit_price | line_total | is_included | breakdown_level |
|----|----------------|----------|-------------|-----------|-------------|----------|------|------------|------------|-------------|-----------------|
| 1 | abc-123 | Electrical | Outlets | GFCI Outlets | Install GFCI outlets | 10 | EA | 45.00 | 450.00 | TRUE | 3 |
| 2 | abc-123 | Electrical | Outlets | Standard | Install standard outlets | 15 | EA | 35.00 | 525.00 | TRUE | 3 |
| 3 | abc-123 | Electrical | Conduit | - | Run 1/2" conduit | 500 | LF | 8.00 | 4000.00 | TRUE | 2 |
| 4 | abc-123 | Demolition | - | - | Remove existing wiring | - | - | - | - | FALSE | 1 |

**AI Consolidation:**
- Rows 1 & 2 (Level 3) → Consolidate to one Level 2 row:
  - Electrical > Outlets: 25 EA @ $39 (average) = $975

**Final stored (after consolidation):**
- Electrical > Outlets: 25 EA @ $39 = $975 (Level 2)
- Electrical > Conduit: 500 LF @ $8 = $4,000 (Level 2)
- Demolition: Excluded (Level 1)

## Benefits

✅ **Unlimited scope items** - No schema changes needed
✅ **Flexible breakdown** - Handles any level of detail
✅ **Historical tracking** - Store unit prices for future estimates
✅ **Included/Excluded** - Separate included items from excluded notes
✅ **AI-ready** - Structure supports consolidation logic

