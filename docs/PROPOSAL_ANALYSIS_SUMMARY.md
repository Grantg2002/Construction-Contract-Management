# Proposal Analysis Summary

## Proposals Analyzed

### 1. HALYARD BID (Metal Framing/Drywall/Ceiling)
**Structure:** Hierarchical + Bulleted
**Breakdown Level:** Level 2 (Category + Subcategory, NO unit pricing)
**Total:** $114,120.00 (single price)

**Pattern:**
- Main categories: Metal Framing, Drywall, Acoustical Ceiling, Insulation
- Subcategories: "20ga @ Interior Walls", "5/8" Type X", "Armstrong Dune #1774"
- **NO unit pricing** - Just descriptions
- Has EXCLUSIONS section (what's NOT included)
- Has INCLUSIONS section

**Example:**
```
• Metal Framing
  o 20ga @ Interior Walls, Hard Lids, & Bulkheads
  o 18ga 8" studs @ Acoustic Ceiling Support
• Drywall
  o 5/8" Type X U.N.O.
  o 5/8" MR Board @ Restrooms
```

---

### 2. Genesis Painting (Paint)
**Structure:** Hierarchical + Bulleted
**Breakdown Level:** Level 2 (Category + Detailed descriptions, section pricing)
**Total:** $14,554.00

**Pattern:**
- Main sections with prices:
  - "Painting Drywall Walls, Ceilings, Bulkheads: $11,850.00"
  - "HM Door Frames: $1,144.00"
  - "Wood Doors: $1,560.00"
- Detailed bullet points under each section
- **NO unit pricing** - Just section totals
- Has assumptions, general requirements, exclusions

**Example:**
```
Painting Drywall Walls, Ceilings, Bulkheads: (Cost Associated: $11,850.00)
- Walk through to verify drywall is acceptable
- Prep and mask all finish items
- Prime walls and bulkheads
- Top coat walls w/ (2) Coats...
```

---

### 3. DeGraaf Fusion (Flooring)
**Structure:** Hierarchical (Table-like)
**Breakdown Level:** Level 2 with SOME unit pricing
**Total:** $26,264.48

**Pattern:**
- Categories: CARPET TILE, VCT
- Subcategories: WALK OFF, ADHESIVE, INSTALL, TRANSITIONS
- **HAS unit pricing:** $3.25/SF, $6.50/SF
- Some items have quantities and unit prices
- Some items are lump sum

**Example:**
```
CARPET TILE CARPET TILE TBD 24X24 COLOR TBD (ALLOWANCE $14,478.75 $3.25/SF)
CARPET TILE WALK OFF CARPET TILE TBD COLOR TBD (ALLOWANCE $585.00 24X24 $6.50/SF)
CARPET TILE FLOOR PREP $500.00
```

---

### 4. Closet Design (Cabinets)
**Structure:** Table format
**Breakdown Level:** Level 1 (Simple items, NO breakdown)
**Total:** $2,964.06

**Pattern:**
- Simple product list: "Cabinet Hardware", "Cabinets"
- Prices per product
- "Price includes" section (what's included)
- "NOT included" items listed

**Example:**
```
Cabinet Hardware    106.33  0.00  6.38  112.71
Cabinets           2,548.42 0.00 152.93 2,701.35
Price includes Breakroom cabinets and countertop
Sink cutout NOT included
```

---

## Key Findings

### Most Proposals Are NOT Broken Down with Unit Pricing

**Patterns Found:**
1. ✅ **Category + Subcategory** (Level 2) - Most common
2. ✅ **Category + Descriptions** (Level 2) - Common
3. ✅ **Simple Items** (Level 1) - Some proposals
4. ❌ **Unit Pricing** - Rare (only DeGraaf has some)

### Common Elements:
- ✅ **Included Items** - Listed in scope
- ✅ **Excluded Items** - Listed separately
- ✅ **Section Prices** - Some have prices per section
- ✅ **Total Price** - Always present
- ✅ **Company Name** - Always present
- ✅ **Date** - Always present

---

## Design Implications

### 1. Scope Storage Strategy

**For proposals WITHOUT unit pricing:**
- Store each item as a row in `scope_items`
- `category` = Main category (e.g., "Metal Framing", "Paint")
- `subcategory` = Subcategory if exists (e.g., "Interior Walls", "Drywall Walls")
- `description` = Full description of work
- `quantity` = NULL (not provided)
- `unit` = NULL (not provided)
- `unit_price` = NULL (not provided)
- `line_total` = NULL (no breakdown)
- `is_included` = TRUE/FALSE

**For proposals WITH unit pricing:**
- Store with full pricing breakdown
- `quantity`, `unit`, `unit_price`, `line_total` filled in

### 2. HTML Scope Generation

**Two-Column Format:**
```
┌─────────────────────────┬─────────────────────────┐
│   INCLUDED ITEMS        │   EXCLUDED ITEMS        │
├─────────────────────────┼─────────────────────────┤
│ • Metal Framing         │ • Any Dumpsters         │
│   o 20ga @ Interior     │ • Any Wood Framing      │
│   o 18ga 8" studs       │ • Any Blocking          │
│                         │                         │
│ • Drywall               │                         │
│   o 5/8" Type X         │                         │
│   o 5/8" MR Board       │                         │
│                         │                         │
│ Total: $114,120.00     │                         │
└─────────────────────────┴─────────────────────────┘
```

### 3. AI Extraction Strategy

**Extract:**
1. Company name
2. Proposal date
3. Total price
4. Categories and subcategories
5. Included items (with descriptions)
6. Excluded items (with descriptions)
7. Section prices (if present)
8. Unit pricing (if present - rare)

**Store:**
- Each included item → Row in `scope_items` with `is_included=TRUE`
- Each excluded item → Row in `scope_items` with `is_included=FALSE`
- Total price → `subcontracts.original_amount`

---

## Next Steps

1. ✅ **Understand patterns** - Done! Most are Level 2, no unit pricing
2. ⏭️ **Design AI prompts** - Extract categories, descriptions, included/excluded
3. ⏭️ **Design HTML generator** - Two-column format
4. ⏭️ **Design consolidation logic** - Handle Level 2 proposals
5. ⏭️ **Build extraction system** - Process proposals into database

---

## Your Insight Confirmed

You're right - **most proposals don't have unit pricing breakdowns**. 

**Solution:**
- Store what's included as individual items (rows)
- Store what's excluded as individual items (rows)
- Store total price at subcontract level
- When unit pricing IS available, store it
- Build historical database from proposals that DO have unit pricing

**This is flexible and handles both cases!** ✅

