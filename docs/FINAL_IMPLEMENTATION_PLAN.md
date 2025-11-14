# Final Implementation Plan - Based on Real Proposal Analysis

## What We Learned from Your Proposals

### Reality Check:
- ✅ Most proposals are **Level 2** (Category + Subcategory)
- ✅ **Rarely have unit pricing** - Just descriptions and totals
- ✅ Have **Included** and **Excluded** sections
- ✅ Some have **section prices** (e.g., "Painting: $11,850")
- ✅ Always have **company name, date, total price**

### Your Insight:
> "They just show all the items and give me an overall price. So maybe we should keep track of what all the overall items are included... Just do breakdowns where you can."

**This is exactly right!** The system needs to:
1. Track **what's included** (even without pricing)
2. Track **what's excluded** (for reference)
3. Store **total price** at subcontract level
4. Extract **unit pricing** when available (rare)
5. Build **historical database** from proposals that DO have pricing

---

## Phase 1: Database Setup ✅ DONE

- ✅ `scope_items` table enhanced with all columns
- ✅ Supports flexible storage (rows, not columns)
- ✅ Handles included/excluded items
- ✅ Supports unit pricing when available

---

## Phase 2: Proposal Upload & Extraction

### Step 2.1: Upload System
**Files:**
- Create: `backend/proposal_upload.py`
- Modify: `backend/main.py` (add upload endpoint)

**Functionality:**
- Accept PDF/Word/Excel uploads
- Store file in Supabase Storage (or local)
- Extract text from file
- Save to `proposals` table

### Step 2.2: AI Extraction
**Files:**
- Modify: `backend/openai_handler.py`

**Extract:**
```python
{
  "company_name": "Halyard",
  "proposal_date": "2025-10-16",
  "total_price": 114120.00,
  "scope_items": [
    {
      "category": "Metal Framing",
      "subcategory": "Interior Walls",
      "description": "20ga @ Interior Walls, Hard Lids, & Bulkheads",
      "is_included": true,
      "has_pricing": false
    },
    {
      "category": "Drywall",
      "subcategory": "Type X",
      "description": "5/8\" Type X U.N.O.",
      "is_included": true,
      "has_pricing": false
    }
  ],
  "excluded_items": [
    {
      "description": "Any Dumpsters",
      "is_included": false
    }
  ]
}
```

### Step 2.3: Store in Database
**Files:**
- Create: `backend/proposal_processor.py`

**Process:**
1. Save proposal to `proposals` table
2. Create subcontract record
3. Save each scope item to `scope_items` table
4. Link everything together

---

## Phase 3: HTML Scope Generation

### Step 3.1: Generate Two-Column HTML
**Files:**
- Create: `backend/scope_html_generator.py`

**Input:** Scope items from database
**Output:** HTML with 2 columns

```html
<table>
  <tr>
    <th>INCLUDED ITEMS</th>
    <th>EXCLUDED ITEMS</th>
  </tr>
  <tr>
    <td>
      <strong>Metal Framing</strong><br>
      • 20ga @ Interior Walls, Hard Lids, & Bulkheads<br>
      • 18ga 8" studs @ Acoustic Ceiling Support<br>
      <br>
      <strong>Drywall</strong><br>
      • 5/8" Type X U.N.O.<br>
      • 5/8" MR Board @ Restrooms<br>
    </td>
    <td>
      • Any Dumpsters<br>
      • Any Wood Framing<br>
      • Any Blocking<br>
      • Any Level 5 Finish<br>
    </td>
  </tr>
</table>
```

---

## Phase 4: Template Filling

### Step 4.1: Fill Template Placeholders
**Files:**
- Create: `backend/template_filler.py`

**Placeholders to Fill:**
- `{{sub.company}}` → From extracted data
- `{{sub.rep}}` → From extracted data (if found)
- `{{sub.street}}`, `{{sub.city}}`, etc. → From extracted data or web research
- `{{project.name}}` → From database
- `{{project.street}}`, etc. → From database
- `{{engineer}}`, `{{architect}}`, etc. → From database
- `{{proposal.date}}` → From extracted data
- `{{proposal.pricing}}` → From extracted data
- `{{scope.html}}` → Generated HTML from scope_items

---

## Phase 5: Word Document Generation

### Step 5.1: Convert HTML to Word
**Files:**
- Create: `backend/word_generator.py`

**Options:**
- Use `mammoth` library (HTML → Word, preserves formatting)
- Or use `python-docx` (manual conversion, more control)

**Output:** `.docx` file with exact template format

---

## Phase 6: Frontend Pages

### Step 6.1: Upload Proposal Page
**Files:**
- Modify: `frontend/src/pages/UploadProposal.jsx`

**Features:**
- File upload (drag & drop)
- Select project
- Upload button
- Progress indicator

### Step 6.2: Proposal Processing Page
**Files:**
- Create: `frontend/src/pages/ProposalProcessing.jsx`

**Features:**
- Show extraction progress
- Display extracted data for review
- Edit extracted items if needed
- Approve and proceed to contract generation

### Step 6.3: Scope Editor Page
**Files:**
- Create: `frontend/src/pages/ScopeEditor.jsx`

**Features:**
- View scope items (included/excluded)
- Edit categories, descriptions
- Add/remove items
- Preview HTML output

### Step 6.4: Contract Generator Page
**Files:**
- Create: `frontend/src/pages/ContractGenerator.jsx`

**Features:**
- Preview filled template
- Generate Word document
- Download contract
- Save to database

---

## Implementation Order

### MVP (Minimum Viable Product):
1. ✅ Database setup (DONE)
2. ⏭️ Upload proposal → Extract text
3. ⏭️ AI extraction → Store in database
4. ⏭️ Manual review/edit extracted data
5. ⏭️ Generate HTML scope
6. ⏭️ Fill template → Generate contract
7. ⏭️ Download contract

### Future Enhancements:
- Web research for missing contact info
- Automatic categorization improvements
- Historical cost database population
- Drawing measurement (future iteration)

---

## Ready to Build?

**Next step:** Start with MVP - Build the upload and extraction system first, then we can test with your actual proposals!

**Should I start coding now, or do you want to review this plan first?**

