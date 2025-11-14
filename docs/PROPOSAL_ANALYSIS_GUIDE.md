# Proposal Analysis Guide

## Ready to Analyze Your Proposals!

I've created a proposal analyzer tool that will:
1. ✅ Extract text from PDFs and Word documents
2. ✅ Analyze breakdown structure (Level 1, 2, or 3)
3. ✅ Identify categories, subcategories, and components
4. ✅ Detect pricing patterns
5. ✅ Understand the structure (hierarchical, table, bulleted)

---

## How to Use

### Step 1: Install Dependencies

```bash
cd backend
pip install pdfplumber python-docx
```

### Step 2: Upload Your Proposals

Place your proposal PDFs in a folder (e.g., `backend/proposals/`) or provide the full path.

**Examples you mentioned:**
- Detailed: Earthworks proposal, Paint Team proposal
- Simple: Drywall proposal, Framing proposal, Suspended Ceiling proposal

### Step 3: Run Analysis

```bash
cd backend
python proposal_analyzer.py proposals/earthworks.pdf proposals/paint_team.pdf proposals/drywall.pdf
```

Or analyze one at a time:
```bash
python proposal_analyzer.py "path/to/your/proposal.pdf"
```

---

## What the Analyzer Will Show

For each proposal, it will analyze:

1. **Breakdown Level Detection:**
   - Level 1: Just categories (e.g., "Electrical Work")
   - Level 2: Category + Subcategory (e.g., "Electrical > Outlets")
   - Level 3: Category + Subcategory + Component (e.g., "Electrical > Outlets > GFCI")

2. **Structure Patterns:**
   - Hierarchical (using >, →, or :)
   - Table format (using | or tabs)
   - Bulleted lists

3. **Pricing Information:**
   - Has dollar amounts?
   - Has quantities?
   - Has units (EA, SF, LF, etc.)?

4. **Sample Content:**
   - First 20 lines for manual review
   - Extracted text preview

---

## After Analysis

Once you upload the proposals and I analyze them, I'll:

1. **Understand the patterns:**
   - How detailed proposals structure their scope
   - How simple proposals structure their scope
   - Common patterns across proposals

2. **Design the AI extraction logic:**
   - How to detect breakdown level
   - How to consolidate Level 3 → Level 2
   - How to categorize items automatically

3. **Create the consolidation rules:**
   - When to consolidate (extremely broken down)
   - When to keep as-is (moderately broken down)
   - How to handle simple proposals

---

## Ready When You Are!

**Just upload your proposal PDFs** and I'll analyze them to understand:
- How Earthworks structures their detailed proposal
- How Paint Team structures their detailed proposal  
- How Drywall/Framing/Suspended Ceiling structure their simple proposals

Then I'll design the AI extraction and consolidation logic based on real examples!

---

## Alternative: Manual Upload

If you prefer, you can:
1. Upload the PDFs to a folder in the project
2. Tell me the file paths
3. I'll analyze them

Or share them directly and I'll analyze them!

