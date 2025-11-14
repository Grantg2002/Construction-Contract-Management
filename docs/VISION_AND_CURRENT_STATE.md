# Vision vs Current State Analysis

## Your Vision (From Your Action Plan)

### Workflow:
1. **Upload Proposal** → Subcontractor sends proposal (various formats)
2. **Extract Information:**
   - Company name
   - Total price
   - Proposal date
   - Scope of work (with pricing breakdown)
   - Included items
   - Excluded items
3. **Handle Pricing Breakdown Levels:**
   - **Extremely broken down** → Consolidate to subcategories only
   - **Moderately broken down** → Use big category + subcategories
   - **Not broken down** → Use main category
4. **AI Analysis:**
   - Consolidate/expand scope as needed
   - Create HTML scope of work (2 columns: Included | Excluded)
   - Fill all template placeholders
5. **Generate Subcontract:**
   - Use Word template (HTML format)
   - Fill all placeholders
   - Create final contract document
6. **Store Historical Data:**
   - Store pricing by work category/subcategory
   - Track: cost per square foot, linear foot, etc.
   - Future: Measure drawings (linear feet walls, square feet, doors, etc.)

---

## Current State (From Supabase Dashboard)

### Tables You Already Have:
1. ✅ `projects`
2. ✅ `subcontracts`
3. ✅ `change_orders`
4. ✅ `drawings` (NEW - not in my original design!)
5. ✅ `draws` (NEW - not in my original design!)
6. ✅ `historical_cost_data`
7. ✅ `invoice_line_items`
8. ✅ `invoices`
9. ✅ `payments`
10. ✅ `scope_items` (NEW - interesting!)
11. ✅ `subcontract_line_items`
12. ✅ `api_usage_log` (for tracking API usage)

### What I Need to Understand:
1. **What columns exist in each table?** (especially `scope_items`, `drawings`, `draws`)
2. **How do these tables relate?** (foreign keys, relationships)
3. **What's the structure of `scope_items`?** (This might be perfect for your vision!)

---

## Gap Analysis

### What You Have That I Didn't Plan For:
- ✅ `scope_items` table - This might be perfect for storing scope breakdown!
- ✅ `drawings` table - For storing project drawings
- ✅ `draws` table - Possibly for payment draws?

### What We Need to Add/Clarify:
1. **Proposal Upload System:**
   - Table to store uploaded proposals
   - File storage (Supabase Storage?)
   - OCR/text extraction capability

2. **Scope Processing Logic:**
   - How to handle different breakdown levels
   - Consolidation rules (extremely broken down → subcategories)
   - HTML generation (2 columns: Included | Excluded)

3. **AI Integration:**
   - Extract company name, price, date
   - Analyze scope breakdown level
   - Consolidate/expand scope as needed
   - Generate HTML scope of work

4. **Template Filling:**
   - Map extracted data to template placeholders
   - Generate HTML with filled placeholders
   - Convert to Word document

5. **Historical Data Storage:**
   - Store pricing by category/subcategory
   - Track units (SF, LF, EA, etc.)
   - Link to projects for context

---

## Questions I Need Answered:

1. **`scope_items` table structure:**
   - What columns does it have?
   - How does it relate to `subcontracts`?
   - Is this where we store the breakdown?

2. **`drawings` table:**
   - What's stored here?
   - Is this for project drawings?
   - Future: Can we measure these for estimates?

3. **`draws` table:**
   - What's this for?
   - Payment draws?
   - How does it relate to invoices/payments?

4. **Current workflow:**
   - Are you manually entering data now?
   - What's the biggest pain point?
   - What do you want automated first?

---

## Next Steps (Planning Phase):

1. **Inspect Your Current Schema:**
   - Get column details for all tables
   - Understand relationships
   - See what data structure you're already using

2. **Map Your Vision to Database:**
   - Where does proposal data go?
   - How do we store scope breakdown?
   - How do we track historical pricing?

3. **Design the Workflow:**
   - Step-by-step: Upload → Extract → Process → Generate → Store
   - What happens at each step?
   - What data flows where?

4. **Identify What to Build:**
   - Frontend: Upload form, proposal viewer, contract generator
   - Backend: API endpoints for each step
   - Database: Any missing tables/columns

5. **Prioritize:**
   - What's MVP (minimum viable product)?
   - What can wait for later iterations?
   - What's the biggest time-saver?

---

## My Recommendation:

**Let's start by understanding your current database structure**, then I'll create a detailed step-by-step plan that:
- Uses your existing tables (especially `scope_items`!)
- Adds only what's missing
- Maps your vision to the actual database
- Prioritizes the biggest pain points first

**Sound good?** Let's inspect your schema first, then I'll create the detailed action plan!

