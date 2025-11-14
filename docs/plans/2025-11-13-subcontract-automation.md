# Subcontract Agreement Automation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a full-stack system that uploads proposals, extracts subcontractor information using AI, researches missing data online, and generates filled Word document contracts using the exact template format.

**Architecture:** 
- Frontend: React app with project navigation, proposal upload, and contract generation
- Backend: FastAPI handles proposal processing, AI extraction, web research, and template filling
- Database: Supabase stores projects, subcontracts, proposals, and extracted data
- Template Engine: Preserves exact Word HTML format while replacing placeholders

**Tech Stack:** 
- FastAPI (Python), React + Vite, Supabase (PostgreSQL), OpenAI API, python-docx (for Word generation), BeautifulSoup/requests (web scraping)

---

## Current State Analysis

### What We Have:
- Basic scaffold with `projects` and `subcontracts` tables (minimal schema)
- Frontend pages: Dashboard, ProjectDetail, UploadProposal
- Backend: Basic FastAPI with OpenAI handler
- Word template: HTML format with placeholders

### What We Need:
1. **Enhanced Database Schema** - Projects need: drawings info, project details (address, engineer, architect, PM), dates
2. **Subcontractor Data Extraction** - AI extracts from proposals: company name, rep, address, contact info
3. **Web Research Module** - Finds missing subcontractor info (office location, phone, email)
4. **Template Processor** - Fills Word HTML template preserving exact format
5. **Word Document Generator** - Converts filled HTML back to .docx format
6. **Enhanced Frontend** - Project detail page shows drawings/info, proposal upload workflow

---

## Placeholder Mapping

From template analysis, these placeholders need to be filled:

**Subcontractor Info:**
- `{{sub.rep}}` - Representative name
- `{{sub.company}}` - Company name
- `{{sub.street}}` - Street address
- `{{sub.city}}` - City
- `{{sub.state}}` - State
- `{{sub.zip}}` - ZIP code
- `{{sub.email}}` - Email address
- `{{sub.phone}}` - Phone number
- `{{sub.fax}}` - Fax number

**Project Info:**
- `{{project.name}}` - Project name
- `{{project.street}}` - Project street address
- `{{project.city}}` - Project city
- `{{project.state}}` - Project state
- `{{project.zip}}` - Project ZIP code
- `{{engineer}}` - Engineer name
- `{{pm.name}}` - Project manager name
- `{{pm.number}}` - Project manager phone
- `{{architect}}` - Architect name
- `{{drawings.date}}` - Drawings date
- `{{engineering.date}}` - Engineering drawings date

**Proposal Info:**
- `{{proposal.date}}` - Proposal date
- `{{proposal.pricing}}` - Contract price/amount
- `{{scope.html}}` - Scope of work (HTML formatted)
- `{{dwg.req}}` / `{{dwg.not_req}}` - Drawings required checkboxes
- `{{AB.req}}` - As-built drawings required checkbox

**Other:**
- `{{current.date}}` - Current date (in header)

---

## Task Breakdown

### Task 1: Inspect and Update Database Schema

**Files:**
- Create: `backend/database_schema.sql`
- Modify: `backend/supabase_client.py` (if needed)

**Step 1: Inspect current Supabase schema**

Run: `cd backend && python inspect_schema.py`
Expected: Shows current table structure or connection error

**Step 2: Create schema migration SQL**

Create `backend/database_schema.sql` with enhanced schema:

```sql
-- Enhanced Projects table
ALTER TABLE projects ADD COLUMN IF NOT EXISTS street TEXT;
ALTER TABLE projects ADD COLUMN IF NOT EXISTS city TEXT;
ALTER TABLE projects ADD COLUMN IF NOT EXISTS state TEXT;
ALTER TABLE projects ADD COLUMN IF NOT EXISTS zip TEXT;
ALTER TABLE projects ADD COLUMN IF NOT EXISTS engineer TEXT;
ALTER TABLE projects ADD COLUMN IF NOT EXISTS architect TEXT;
ALTER TABLE projects ADD COLUMN IF NOT EXISTS pm_name TEXT;
ALTER TABLE projects ADD COLUMN IF NOT EXISTS pm_phone TEXT;
ALTER TABLE projects ADD COLUMN IF NOT EXISTS drawings_date DATE;
ALTER TABLE projects ADD COLUMN IF NOT EXISTS engineering_date DATE;

-- Proposals table (new)
CREATE TABLE IF NOT EXISTS proposals (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  filename TEXT NOT NULL,
  content TEXT,
  uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  processed_at TIMESTAMP WITH TIME ZONE
);

-- Extracted subcontractor data table (new)
CREATE TABLE IF NOT EXISTS subcontractor_data (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  proposal_id UUID REFERENCES proposals(id) ON DELETE CASCADE,
  company_name TEXT,
  representative_name TEXT,
  street TEXT,
  city TEXT,
  state TEXT,
  zip TEXT,
  email TEXT,
  phone TEXT,
  fax TEXT,
  proposal_date DATE,
  proposal_amount DECIMAL(10, 2),
  scope_of_work_html TEXT,
  drawings_required BOOLEAN,
  as_built_required BOOLEAN,
  extracted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  research_completed BOOLEAN DEFAULT FALSE
);
```

**Step 3: Verify schema**

Run migration in Supabase SQL Editor or via script

---

### Task 2: Create Web Research Module

**Files:**
- Create: `backend/web_research.py`

**Step 1: Create web research handler**

```python
"""
Web research module to find subcontractor information
"""
import requests
from bs4 import BeautifulSoup
import re
from typing import Dict, Optional
import time

def search_subcontractor_info(company_name: str) -> Dict[str, Optional[str]]:
    """
    Search for subcontractor company information online
    
    Args:
        company_name: Name of the subcontractor company
        
    Returns:
        Dictionary with found information (address, phone, email, etc.)
    """
    results = {
        "street": None,
        "city": None,
        "state": None,
        "zip": None,
        "phone": None,
        "email": None,
        "fax": None
    }
    
    # Use Google search (or other search engine API)
    # For now, placeholder - will use Google Custom Search API or web scraping
    search_query = f"{company_name} construction contact information"
    
    # TODO: Implement actual web search and parsing
    # This is a placeholder structure
    
    return results

def extract_contact_info_from_text(text: str) -> Dict[str, Optional[str]]:
    """
    Extract contact information from text using regex patterns
    """
    info = {
        "phone": None,
        "email": None,
        "address": None
    }
    
    # Phone pattern (US format)
    phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    phone_match = re.search(phone_pattern, text)
    if phone_match:
        info["phone"] = phone_match.group()
    
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_match = re.search(email_pattern, text)
    if email_match:
        info["email"] = email_match.group()
    
    return info
```

**Step 2: Add dependencies**

Update `backend/requirements.txt`:
```
beautifulsoup4==4.12.2
requests==2.31.0
```

---

### Task 3: Enhance OpenAI Handler for Proposal Extraction

**Files:**
- Modify: `backend/openai_handler.py`

**Step 1: Update process_proposal function**

```python
async def extract_subcontractor_info(proposal_content: str) -> Dict[str, Any]:
    """
    Extract subcontractor information from proposal using OpenAI
    
    Args:
        proposal_content: Text content of the proposal document
        
    Returns:
        Dictionary with extracted subcontractor data
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY must be set")
    
    extraction_prompt = f"""
    Extract subcontractor information from this proposal. Return ONLY a JSON object with these fields:
    {{
        "company_name": "company name",
        "representative_name": "contact person name",
        "street": "street address",
        "city": "city",
        "state": "state abbreviation",
        "zip": "zip code",
        "email": "email address if found",
        "phone": "phone number if found",
        "fax": "fax number if found",
        "proposal_date": "date in YYYY-MM-DD format",
        "proposal_amount": "dollar amount as number",
        "scope_of_work": "detailed scope description",
        "drawings_required": true/false,
        "as_built_required": true/false
    }}
    
    Proposal content:
    {proposal_content}
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are an expert at extracting structured data from construction proposals. Always return valid JSON only."
            },
            {
                "role": "user",
                "content": extraction_prompt
            }
        ],
        response_format={"type": "json_object"}
    )
    
    import json
    extracted_data = json.loads(response.choices[0].message.content)
    
    return extracted_data
```

---

### Task 4: Create Template Processor

**Files:**
- Create: `backend/template_processor.py`

**Step 1: Create template filling function**

```python
"""
Template processor for filling Word document placeholders
"""
import re
from typing import Dict
from datetime import datetime

def fill_template(template_path: str, data: Dict[str, any]) -> str:
    """
    Fill template placeholders with data while preserving exact HTML format
    
    Args:
        template_path: Path to HTML template file
        data: Dictionary with placeholder values
        
    Returns:
        Filled HTML content as string
    """
    # Read template
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Add current date if not provided
    if 'current.date' not in data:
        data['current.date'] = datetime.now().strftime('%B %d, %Y')
    
    # Replace placeholders - handle nested HTML tags in placeholders
    # Pattern matches {{placeholder}} even if wrapped in HTML tags
    pattern = r'\{\{([^}]+)\}\}'
    
    def replace_placeholder(match):
        placeholder = match.group(1).strip()
        # Remove HTML tags from placeholder name
        clean_placeholder = re.sub(r'<[^>]+>', '', placeholder)
        clean_placeholder = re.sub(r'class=[^>]+', '', clean_placeholder)
        clean_placeholder = clean_placeholder.strip()
        
        # Map placeholder to data
        value = data.get(clean_placeholder, '')
        
        # Handle checkbox placeholders
        if placeholder in ['dwg.req', 'AB.req']:
            if data.get(clean_placeholder, False):
                return '[X]'
            return '[ ]'
        if placeholder == 'dwg.not_req':
            if not data.get('drawings_required', True):
                return '[X]'
            return '[ ]'
        
        return str(value) if value else ''
    
    filled_template = re.sub(pattern, replace_placeholder, template)
    
    return filled_template
```

---

### Task 5: Create Word Document Generator

**Files:**
- Create: `backend/word_generator.py`
- Modify: `backend/requirements.txt`

**Step 1: Add python-docx dependency**

Update `backend/requirements.txt`:
```
python-docx==1.1.0
```

**Step 2: Create Word generator**

```python
"""
Generate Word documents from filled HTML templates
"""
from docx import Document
from docx.shared import Inches
import html2text
from bs4 import BeautifulSoup

def html_to_word(html_content: str, output_path: str):
    """
    Convert HTML content to Word document
    
    Args:
        html_content: HTML string with filled placeholders
        output_path: Path to save .docx file
    """
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Create Word document
    doc = Document()
    
    # Extract and add content preserving tables and formatting
    # This is simplified - may need more sophisticated conversion
    for table in soup.find_all('table'):
        word_table = doc.add_table(rows=0, cols=0)
        word_table.style = 'Table Grid'
        
        for row in table.find_all('tr'):
            cells = row.find_all(['td', 'th'])
            if cells:
                word_row = word_table.add_row()
                for i, cell in enumerate(cells):
                    if i < len(word_row.cells):
                        word_row.cells[i].text = cell.get_text(strip=True)
    
    # Save document
    doc.save(output_path)
```

**Note:** HTML to Word conversion is complex. May need to use `mammoth` library or `pandoc` for better conversion.

---

### Task 6: Create Backend API Endpoints

**Files:**
- Modify: `backend/main.py`

**Step 1: Add new endpoints**

```python
@app.post("/api/process-proposal")
async def process_proposal_endpoint(
    project_id: str,
    file: UploadFile = File(...)
):
    """
    Upload proposal, extract data, research info, generate contract
    """
    # 1. Save proposal to database
    # 2. Extract subcontractor info using AI
    # 3. Research missing info online
    # 4. Fill template
    # 5. Generate Word doc
    # 6. Return download link
    
    pass

@app.get("/api/generate-contract/{proposal_id}")
async def generate_contract(proposal_id: str):
    """
    Generate contract document from processed proposal
    """
    pass
```

---

### Task 7: Update Frontend - Enhanced Project Detail Page

**Files:**
- Modify: `frontend/src/pages/ProjectDetail.jsx`

**Step 1: Add project info display**

Show project details: address, engineer, architect, PM, drawing dates

**Step 2: Add proposal upload section**

Allow uploading proposals for this project

---

### Task 8: Update Frontend - Proposal Processing Workflow

**Files:**
- Modify: `frontend/src/pages/UploadProposal.jsx`
- Create: `frontend/src/pages/ProposalProcessing.jsx`

**Step 1: Create processing status page**

Show progress: Uploading → Extracting → Researching → Generating

---

## Next Steps

1. **Get Supabase credentials** - User provides URL and API key
2. **Run schema inspection** - Verify current database structure
3. **Execute tasks in order** - Follow plan step-by-step
4. **Test each component** - Verify functionality before moving on

---

## Notes

- Template format must be preserved exactly - no HTML structure changes
- Web research may need API keys (Google Custom Search, etc.)
- Word document generation may need refinement for complex tables
- Consider using `mammoth` library for better HTML→Word conversion

