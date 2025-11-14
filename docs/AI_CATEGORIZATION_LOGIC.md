# AI Categorization Logic

## How AI Will Parse and Categorize Proposals

### ✅ Confirmed: Structure is Ready

Your `scope_items` table now has:
- `category` - Level 1 (e.g., "Electrical", "Earthworks", "Paint")
- `subcategory` - Level 2 (e.g., "Outlets", "Excavation", "Interior Paint")
- `component` - Level 3 (e.g., "GFCI Outlets", "Topsoil Removal", "Primer Coat")

**The AI will automatically:**
1. ✅ Parse proposal text
2. ✅ Identify work items
3. ✅ Categorize into existing buckets (category/subcategory/component)
4. ✅ **Create new buckets** if it encounters something novel
5. ✅ Extract pricing, quantities, units

---

## Categorization Process

### Step 1: Extract Work Items
AI reads proposal and identifies:
- Work descriptions
- Quantities
- Units
- Prices

### Step 2: Categorize Each Item

**Example: "Install 25 GFCI outlets @ $45 each"**

AI determines:
- **Category:** "Electrical" (matches existing or creates new)
- **Subcategory:** "Outlets" (matches existing or creates new)
- **Component:** "GFCI Outlets" (matches existing or creates new)
- **Quantity:** 25
- **Unit:** EA
- **Unit Price:** $45
- **Line Total:** $1,125

### Step 3: Handle Novel Items

**If AI encounters something new:**
- "Install solar panel system" → Creates new category "Solar"
- "Install smart home automation" → Creates new category "Automation"
- "Install EV charging station" → Creates new category "EV Infrastructure"

**The system is flexible** - no pre-defined categories needed!

---

## Breakdown Level Detection

### Level 3 (Extremely Broken Down)
**Example:**
```
Electrical
  ├─ Outlets
  │   ├─ GFCI Outlets: 10 EA @ $45
  │   ├─ Standard Outlets: 15 EA @ $35
  │   └─ USB Outlets: 5 EA @ $65
  └─ Conduit
      ├─ 1/2" Conduit: 200 LF @ $8
      └─ 3/4" Conduit: 300 LF @ $10
```

**AI Action:** Consolidate to Level 2
- Electrical > Outlets: 30 EA @ $43.33 (average)
- Electrical > Conduit: 500 LF @ $9.20 (average)

### Level 2 (Moderately Broken Down)
**Example:**
```
Electrical
  ├─ Outlets: $1,300
  ├─ Conduit: $4,000
  └─ Panel: $2,500
```

**AI Action:** Keep as Level 2 (no consolidation needed)

### Level 1 (Not Broken Down)
**Example:**
```
Electrical Work: $7,800
```

**AI Action:** Keep as Level 1 (category only)

---

## Consolidation Rules

### Rule 1: Extremely Broken Down → Consolidate
**If:** Multiple components under same subcategory
**Then:** Consolidate to subcategory level
**Example:**
- GFCI Outlets + Standard Outlets + USB Outlets
- → Single line: "Outlets" with averaged pricing

### Rule 2: Moderately Broken Down → Keep As-Is
**If:** Category + Subcategory structure
**Then:** Keep separate lines for each subcategory
**Example:**
- Keep: Outlets, Conduit, Panel as separate lines

### Rule 3: Not Broken Down → Keep As-Is
**If:** Just category level
**Then:** Keep single line
**Example:**
- Keep: "Electrical Work" as single line

---

## What I'll Learn from Your Proposals

When you upload:
1. **Earthworks proposal** (detailed)
   - How they structure Level 3 breakdown
   - What categories/subcategories they use
   - How pricing is presented

2. **Paint Team proposal** (detailed)
   - Their breakdown structure
   - How they categorize work
   - Pricing format

3. **Drywall/Framing/Suspended Ceiling** (simple)
   - How simple proposals are structured
   - What level of detail they provide
   - How to handle minimal breakdown

**Then I'll:**
- Design AI prompts for extraction
- Create consolidation logic
- Build categorization rules
- Test with your actual proposals

---

## Next Steps

1. ✅ **Structure ready** - `scope_items` table has all needed columns
2. ⏳ **Upload proposals** - Share your PDFs
3. ⏳ **Analyze patterns** - I'll analyze each proposal
4. ⏳ **Design AI logic** - Based on real examples
5. ⏳ **Build extraction system** - Automated proposal processing

**Ready for your proposals!** Upload them and I'll analyze the patterns! 🚀

