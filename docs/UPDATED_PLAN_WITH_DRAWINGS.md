# Updated Implementation Plan - With Drawings Management

## Key Updates Based on Your Feedback

### 1. Drawings Management ✅ ADDED
- Upload architectural drawings (with date)
- Upload engineering drawings (with date)
- Store in `drawings` table
- Link to projects
- Handle revisions (update dates)
- Use dates for template placeholders: `{{drawings.date}}`, `{{engineering.date}}`

### 2. Scope Storage Strategy ✅ UPDATED
**If NO itemized pricing:**
- Store as **ONE row** per category/subcategory
- `description` = Full scope description (all items included)
- Don't create rows for each individual item
- Example: "Metal Framing: 20ga @ Interior Walls, 18ga 8" studs @ Acoustic Ceiling Support"

**If HAS itemized pricing:**
- Store individual rows with pricing breakdown

### 3. HTML Format ✅ UPDATED
- **NO table** - Just HTML divs with CSS columns
- Two columns: Included | Excluded
- No borders, no outlines
- Clean spacing and page breaks

---

## Updated Database Schema

### Drawings Table (Already exists, enhance it)
```sql
-- Enhance drawings table
ALTER TABLE drawings
  ADD COLUMN IF NOT EXISTS project_id UUID REFERENCES projects(id),
  ADD COLUMN IF NOT EXISTS drawing_type TEXT, -- 'architectural' or 'engineering'
  ADD COLUMN IF NOT EXISTS drawing_date DATE,
  ADD COLUMN IF NOT EXISTS revision_number TEXT,
  ADD COLUMN IF NOT EXISTS file_url TEXT,
  ADD COLUMN IF NOT EXISTS architect_name TEXT, -- For architectural drawings
  ADD COLUMN IF NOT EXISTS engineer_name TEXT;  -- For engineering drawings
```

---

## Updated Workflow

### Step 1: Project Setup
1. Create project
2. Upload architectural drawings → Store date, architect name
3. Upload engineering drawings → Store date, engineer name
4. Set project manager, engineer, architect info

### Step 2: Proposal Upload
1. Upload proposal PDF
2. Extract: company, date, total price, scope
3. **If no itemized pricing:** Store scope as ONE row per category with full description
4. **If has itemized pricing:** Store individual rows

### Step 3: Contract Generation
1. Fill template placeholders:
   - `{{drawings.date}}` → Latest architectural drawing date
   - `{{engineering.date}}` → Latest engineering drawing date
   - `{{architect}}` → From drawings or project
   - `{{engineer}}` → From drawings or project
   - `{{scope.html}}` → Generated HTML (NO table, just divs)

---

## HTML Scope Format (Updated)

**NO TABLE - Just CSS columns:**

```html
<div style="display: flex; gap: 20px;">
  <div style="flex: 1;">
    <h3>INCLUDED ITEMS</h3>
    <p><strong>Metal Framing</strong></p>
    <p>20ga @ Interior Walls, Hard Lids, & Bulkheads<br>
    18ga 8" studs @ Acoustic Ceiling Support</p>
    
    <p><strong>Drywall</strong></p>
    <p>5/8" Type X U.N.O.<br>
    5/8" MR Board @ Restrooms<br>
    Walls: Level 4 U.N.O.<br>
    Ceilings: Level 4 U.N.O.</p>
  </div>
  
  <div style="flex: 1;">
    <h3>EXCLUDED ITEMS</h3>
    <p>• Any Dumpsters<br>
    • Any Wood Framing<br>
    • Any Blocking<br>
    • Any Level 5 Finish</p>
  </div>
</div>
```

**Clean, no borders, just spacing!**

---

## Updated Scope Storage Logic

### Example: HALYARD Proposal

**Current approach (WRONG - too many rows):**
- Row 1: Metal Framing > Interior Walls > "20ga @ Interior Walls"
- Row 2: Metal Framing > Interior Walls > "Hard Lids"
- Row 3: Metal Framing > Interior Walls > "Bulkheads"
- ... (too many rows!)

**New approach (CORRECT - consolidated):**
- Row 1: 
  - category = "Metal Framing"
  - subcategory = "Interior Walls"
  - description = "20ga @ Interior Walls, Hard Lids, & Bulkheads"
  - (no pricing breakdown)

- Row 2:
  - category = "Metal Framing"
  - subcategory = "Acoustic Ceiling Support"
  - description = "18ga 8" studs @ Acoustic Ceiling Support (Required due to 36' span)"
  - (no pricing breakdown)

- Row 3:
  - category = "Drywall"
  - subcategory = "Type X"
  - description = "5/8" Type X U.N.O."
  - (no pricing breakdown)

**Much cleaner!** One row per logical grouping.

---

## Implementation Steps

### Phase 1: Drawings Management
1. Enhance `drawings` table
2. Create upload drawings page
3. Store drawing dates
4. Link to projects

### Phase 2: Proposal Upload & Extraction
1. Upload proposal
2. AI extraction (consolidate scope into logical rows)
3. Store in database (one row per category/subcategory)

### Phase 3: HTML Generation
1. Generate HTML scope (NO table, CSS columns)
2. Format included/excluded items
3. Clean spacing

### Phase 4: Template Filling
1. Fill all placeholders (including drawing dates)
2. Generate contract

---

## Ready to Build MVP!

Starting with:
1. Drawings management
2. Updated scope storage logic
3. HTML generation (no table)
4. Proposal upload & extraction

Let's go! 🚀

