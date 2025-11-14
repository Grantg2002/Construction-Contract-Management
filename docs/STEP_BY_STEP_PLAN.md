# Step-by-Step Implementation Plan

## Phase 1: Understanding Current State

### Step 1.1: Document Your Current Database Structure
**What I need from you:**
- Open each table in Supabase Table Editor
- Tell me what columns exist in these key tables:
  - `scope_items` (especially important!)
  - `subcontracts`
  - `projects`
  - `drawings`
  - `draws`

**OR** you can:
- Click on each table → Click "View table structure" or "Columns" 
- Share a screenshot or list the columns

**Why this matters:**
- I need to see if `scope_items` already has the structure for your scope breakdown vision
- I need to understand how tables relate to each other
- I need to know what columns already exist vs what we need to add

---

## Phase 2: Mapping Your Vision to Database

### Your Workflow (As I Understand It):

```
1. SUBCONTRACTOR SENDS PROPOSAL
   ↓
2. YOU UPLOAD PROPOSAL (PDF, Word, Excel, etc.)
   ↓
3. SYSTEM EXTRACTS:
   - Company name
   - Total price
   - Proposal date
   - Scope breakdown (various levels of detail)
   ↓
4. AI ANALYZES SCOPE BREAKDOWN LEVEL:
   - Extremely broken down? → Consolidate to subcategories
   - Moderately broken down? → Use category + subcategories
   - Not broken down? → Use main category
   ↓
5. AI CREATES HTML SCOPE OF WORK:
   - 2 columns: Included Items | Excluded Items
   - With prices for included items
   - Notes for excluded items
   ↓
6. FILL TEMPLATE PLACEHOLDERS:
   - All subcontractor info
   - All project info
   - Scope HTML (2 columns)
   - Pricing
   ↓
7. GENERATE CONTRACT:
   - Use Word template (HTML format)
   - Fill all placeholders
   - Create final .docx file
   ↓
8. STORE IN DATABASE:
   - Save contract to subcontracts table
   - Save scope breakdown to scope_items (or subcontract_line_items)
   - Save pricing data to historical_cost_data
```

---

## Phase 3: Database Design Questions

### Key Questions:

1. **`scope_items` table:**
   - What columns does it have?
   - Does it store: category, subcategory, description, price, quantity, unit?
   - How does it link to `subcontracts`?

2. **Scope Breakdown Levels:**
   - **Level 1:** Main category only (e.g., "Electrical Work")
   - **Level 2:** Category + Subcategory (e.g., "Electrical > Outlets")
   - **Level 3:** Category + Subcategory + Component (e.g., "Electrical > Outlets > GFCI Outlets")
   
   **Your Rules:**
   - Level 3 (extremely broken down) → Consolidate to Level 2 (subcategories)
   - Level 2 (moderately broken down) → Keep as is
   - Level 1 (not broken down) → Keep as is

3. **HTML Scope Generation:**
   - 2 columns: Included | Excluded
   - Included: Items with prices
   - Excluded: Items without prices (just notes)
   - Format: Bullet points? Tables? How should it look?

4. **Historical Data Storage:**
   - Store by: Category, Subcategory, Unit (SF, LF, EA), Price
   - Link to: Project, Subcontractor, Date
   - Future: Link to drawing measurements (linear feet, square feet, etc.)

---

## Phase 4: Implementation Steps (Draft)

### Step 4.1: Proposal Upload System
- **Frontend:** Upload form (drag & drop)
- **Backend:** File storage (Supabase Storage)
- **Database:** `proposals` table (if doesn't exist)
  - Columns: id, project_id, filename, file_url, uploaded_at, status

### Step 4.2: Text Extraction
- **Backend:** Extract text from PDF/Word/Excel
- **Libraries:** pdfplumber, python-docx, openpyxl
- **Store:** Raw text in `proposals.content` or `proposals.ocr_text`

### Step 4.3: AI Extraction
- **Backend:** OpenAI API call
- **Extract:**
  - Company name
  - Total price
  - Proposal date
  - Scope breakdown (with levels detected)
- **Store:** In `subcontractor_data` table (or directly in `subcontracts`)

### Step 4.4: Scope Processing Logic
- **Backend:** Python function
- **Input:** Extracted scope breakdown
- **Process:**
  - Detect breakdown level (1, 2, or 3)
  - Apply consolidation rules
  - Separate included vs excluded items
- **Output:** Structured scope data

### Step 4.5: HTML Scope Generation
- **Backend:** Template engine
- **Input:** Processed scope data
- **Output:** HTML with 2 columns
  ```html
  <table>
    <tr>
      <td>INCLUDED ITEMS</td>
      <td>EXCLUDED ITEMS</td>
    </tr>
    <tr>
      <td>
        • Item 1 - $100
        • Item 2 - $200
      </td>
      <td>
        • Not included: Item X
        • Not included: Item Y
      </td>
    </tr>
  </table>
  ```

### Step 4.6: Template Filling
- **Backend:** Template processor
- **Input:** 
  - Subcontractor data
  - Project data (from database)
  - Scope HTML
  - Pricing
- **Output:** Filled HTML template

### Step 4.7: Word Document Generation
- **Backend:** HTML to Word converter
- **Options:**
  - `python-docx` (manual conversion)
  - `mammoth` (HTML to Word)
  - `pandoc` (external tool)
- **Output:** .docx file

### Step 4.8: Database Storage
- **Save to:**
  - `subcontracts` table (main contract)
  - `scope_items` or `subcontract_line_items` (scope breakdown)
  - `historical_cost_data` (pricing for future estimates)

---

## Phase 5: Frontend Pages Needed

1. **Dashboard** (exists) - List projects
2. **Project Detail** (exists) - Show project info, subcontracts
3. **Upload Proposal** (needs enhancement) - Upload proposal file
4. **Proposal Processing** (NEW) - Show extraction progress, review extracted data
5. **Scope Editor** (NEW) - Review/edit scope breakdown before generating contract
6. **Contract Generator** (NEW) - Review filled template, generate Word doc
7. **Contract Viewer** (NEW) - View generated contracts

---

## Next Steps (Before Coding):

1. **You share:** Column structure of key tables (especially `scope_items`)
2. **We discuss:** How scope breakdown should be stored
3. **We finalize:** Database schema (what to add/modify)
4. **We prioritize:** What to build first (MVP)
5. **We code:** Step by step, starting with MVP

---

## Questions for You:

1. **Can you share the column structure of `scope_items` table?** (This is critical!)

2. **For scope HTML generation:**
   - Should it be a table with 2 columns?
   - Or two separate sections?
   - What styling/formatting do you want?

3. **Priority:**
   - What's the biggest pain point right now?
   - What would save you the most time if automated first?

4. **Proposal formats:**
   - What formats do you typically receive? (PDF, Word, Excel, handwritten?)
   - Which is most common?

5. **Scope breakdown:**
   - Can you give me an example of:
     - Extremely broken down proposal?
     - Moderately broken down proposal?
     - Not broken down proposal?
   - So I can understand the consolidation logic better?

---

**Ready when you are!** Share the table structures and we'll finalize the plan! 🚀

