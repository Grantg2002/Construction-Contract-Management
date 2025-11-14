# Database Design: Flexible Scope Items Storage

## ❌ WRONG Approach: Columns for Each Scope Item

**Don't do this:**
```sql
CREATE TABLE subcontracts (
  id UUID,
  electrical_work DECIMAL(10,2),
  plumbing_work DECIMAL(10,2),
  hvac_work DECIMAL(10,2),
  framing_work DECIMAL(10,2),
  drywall_work DECIMAL(10,2),
  -- ... hundreds more columns? NO!
);
```

**Problems:**
- ❌ Need to know ALL possible scope items upfront
- ❌ Must alter table schema every time you see something new
- ❌ Extremely time-intensive
- ❌ Not flexible or nimble
- ❌ Can't handle variations easily

---

## ✅ CORRECT Approach: Rows in a Table

**Do this instead:**
```sql
CREATE TABLE scope_items (
  id UUID PRIMARY KEY,
  subcontract_id UUID REFERENCES subcontracts(id),
  
  -- Flexible fields that work for ANY scope item
  category TEXT,           -- e.g., "Electrical"
  subcategory TEXT,        -- e.g., "Outlets"
  description TEXT,        -- e.g., "Install GFCI outlets"
  quantity DECIMAL(10,2),  -- e.g., 25
  unit TEXT,               -- e.g., "EA" (each), "SF" (square feet), "LF" (linear feet)
  unit_price DECIMAL(10,2), -- e.g., 45.00
  line_total DECIMAL(12,2), -- quantity * unit_price
  
  -- Included/Excluded flag
  is_included BOOLEAN DEFAULT TRUE, -- TRUE = included, FALSE = excluded
  
  -- Ordering
  display_order INTEGER,
  
  created_at TIMESTAMP
);
```

**Benefits:**
- ✅ **Unlimited scope items** - Add as many rows as needed
- ✅ **No schema changes** - New items = new rows, not new columns
- ✅ **Flexible** - Works for ANY type of work
- ✅ **Nimble** - System adapts automatically
- ✅ **Queryable** - Easy to search, filter, group by category

---

## How It Works in Practice

### Example: Electrical Proposal

**Proposal has:**
- Install outlets: 25 EA @ $45 = $1,125
- Run conduit: 500 LF @ $8 = $4,000
- Install panel: 1 EA @ $2,500 = $2,500
- **Excluded:** Demolition work

**Stored as ROWS in `scope_items`:**

| id | subcontract_id | category | subcategory | description | quantity | unit | unit_price | line_total | is_included |
|----|---------------|----------|-------------|-------------|----------|------|------------|------------|-------------|
| 1  | abc-123       | Electrical | Outlets | Install GFCI outlets | 25 | EA | 45.00 | 1125.00 | TRUE |
| 2  | abc-123       | Electrical | Conduit | Run 1/2" conduit | 500 | LF | 8.00 | 4000.00 | TRUE |
| 3  | abc-123       | Electrical | Panel | Install 200A panel | 1 | EA | 2500.00 | 2500.00 | TRUE |
| 4  | abc-123       | Demolition | - | Remove existing wiring | - | - | - | - | FALSE |

**No new columns needed!** Just new rows.

---

## Your `scope_items` Table Structure

Based on your vision, your `scope_items` table should have:

```sql
CREATE TABLE scope_items (
  id UUID PRIMARY KEY,
  subcontract_id UUID REFERENCES subcontracts(id),
  
  -- Hierarchy (for consolidation logic)
  category TEXT,              -- Level 1: "Electrical"
  subcategory TEXT,           -- Level 2: "Outlets" 
  component TEXT,             -- Level 3: "GFCI Outlets" (optional, for extremely broken down)
  
  -- Item Details
  description TEXT NOT NULL,
  quantity DECIMAL(10,2),
  unit TEXT,                  -- EA, SF, LF, HR, etc.
  unit_price DECIMAL(10,2),
  line_total DECIMAL(12,2),
  
  -- Included/Excluded
  is_included BOOLEAN DEFAULT TRUE,
  
  -- Consolidation Level (for your AI logic)
  breakdown_level INTEGER,    -- 1 = category only, 2 = category+subcategory, 3 = all levels
  
  -- Display
  display_order INTEGER,
  
  -- Timestamps
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## How AI Consolidation Works

### Scenario 1: Extremely Broken Down (Level 3)
**Input from Proposal:**
- Electrical > Outlets > GFCI Outlets: 10 EA @ $45
- Electrical > Outlets > Standard Outlets: 15 EA @ $35
- Electrical > Outlets > USB Outlets: 5 EA @ $65

**AI Consolidates to Level 2:**
- Electrical > Outlets: 30 EA @ $43.33 (average) = $1,300

**Stored as ONE row:**
```sql
INSERT INTO scope_items (category, subcategory, description, quantity, unit, unit_price, line_total, breakdown_level)
VALUES ('Electrical', 'Outlets', 'Install various outlet types', 30, 'EA', 43.33, 1300.00, 2);
```

### Scenario 2: Moderately Broken Down (Level 2)
**Input from Proposal:**
- Electrical > Outlets: $1,300
- Electrical > Conduit: $4,000
- Electrical > Panel: $2,500

**AI Keeps as Level 2:**
- Stored as 3 separate rows (one for each subcategory)

### Scenario 3: Not Broken Down (Level 1)
**Input from Proposal:**
- Electrical Work: $7,800

**AI Keeps as Level 1:**
- Stored as ONE row with category only, no subcategory

---

## HTML Generation from Rows

**Query scope items:**
```sql
SELECT * FROM scope_items 
WHERE subcontract_id = 'abc-123'
ORDER BY is_included DESC, display_order;
```

**Generate HTML:**

```html
<table>
  <tr>
    <th>INCLUDED ITEMS</th>
    <th>EXCLUDED ITEMS</th>
  </tr>
  <tr>
    <td>
      <ul>
        <li>Electrical > Outlets: 30 EA @ $43.33 = $1,300</li>
        <li>Electrical > Conduit: 500 LF @ $8.00 = $4,000</li>
        <li>Electrical > Panel: 1 EA @ $2,500 = $2,500</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>Demolition work not included</li>
      </ul>
    </td>
  </tr>
</table>
```

**Generated dynamically** - No hardcoding needed!

---

## Historical Cost Database

**From completed contracts, extract pricing:**

```sql
-- After contract is completed, populate historical_cost_data
INSERT INTO historical_cost_data (work_category, work_type, unit, unit_price, project_location, project_year)
SELECT 
  category,
  subcategory,
  unit,
  AVG(unit_price) as avg_unit_price,
  (SELECT city FROM projects WHERE id = (SELECT project_id FROM subcontracts WHERE id = scope_items.subcontract_id)),
  EXTRACT(YEAR FROM (SELECT created_at FROM subcontracts WHERE id = scope_items.subcontract_id))
FROM scope_items
WHERE is_included = TRUE
  AND unit_price IS NOT NULL
GROUP BY category, subcategory, unit;
```

**Query for estimates:**
```sql
-- "What did electrical outlets cost per EA in previous projects?"
SELECT AVG(unit_price), COUNT(*) as sample_size
FROM historical_cost_data
WHERE work_category = 'Electrical'
  AND work_type = 'Outlets'
  AND unit = 'EA';
```

---

## Answer to Your Question

### Q: Can the system create new columns for novel scope items?

**A: NO - and you DON'T WANT IT TO!**

Instead:
- ✅ **New scope items = New rows** (not new columns)
- ✅ **System is automatically flexible** - handles ANY scope item
- ✅ **No schema changes needed** - works for everything
- ✅ **Nimble and adaptable** - exactly what you want!

### Your `scope_items` Table Already Solves This!

If your `scope_items` table has columns like:
- `category`
- `subcategory` 
- `description`
- `quantity`
- `unit`
- `unit_price`

Then it's **already flexible** and can handle:
- ✅ Electrical work
- ✅ Plumbing work
- ✅ Framing work
- ✅ **ANY new type of work** you've never seen before
- ✅ **ANY combination** of categories/subcategories

**No new columns needed!** Just insert new rows.

---

## Next Steps

1. **Check your `scope_items` table structure**
   - Does it have: category, subcategory, description, quantity, unit, price?
   - If yes → Perfect! It's already flexible
   - If no → We'll add those columns (one-time setup)

2. **Confirm the structure works for your vision**
   - Can it store included vs excluded items?
   - Can it handle different breakdown levels?
   - Can it store pricing for historical data?

3. **Build the system**
   - AI extracts scope → Creates rows in `scope_items`
   - HTML generator → Reads rows, creates HTML
   - Historical data → Extracts from rows

---

## Summary

**You asked:** "Do I need to create columns for every scope item?"

**Answer:** **NO!** Use rows in a `scope_items` table. This is:
- ✅ Standard database design
- ✅ Flexible and nimble
- ✅ Handles unlimited scope items
- ✅ No schema changes needed
- ✅ Perfect for your use case

**Your `scope_items` table (if structured correctly) already solves this problem!**

