# Drawing Management - Simplified Approach

## Overview
Store architectural and engineering drawings with metadata (architect, engineer, dates) for use in contract generation. No schedule extraction needed for now.

## What We Store

### Drawing Metadata
- **Architectural Drawings:**
  - Drawing date
  - Architect name
  - Revision number (optional)
  - File reference

- **Engineering Drawings:**
  - Drawing date
  - Engineer name
  - Revision number (optional)
  - File reference

## How It Works

### 1. Upload Drawing
When you upload a drawing:
- Enter drawing type (architectural or engineering)
- Enter drawing date
- Enter architect name (for architectural) or engineer name (for engineering)
- File is stored
- **Project's drawing dates are automatically updated** (via database trigger)

### 2. Upload Revised Drawings
When you upload a new revision:
- Upload new drawing file
- Enter new date
- Enter architect/engineer name
- New drawing becomes "current"
- Old drawing is marked as not current
- **Project dates are updated automatically**

### 3. Use in Contracts
When generating contracts:
- Template filler automatically uses:
  - Latest architectural drawing date → `{{drawings.date}}`
  - Latest engineering drawing date → `{{engineering.date}}`
  - Architect name → `{{architect}}`
  - Engineer name → `{{engineer}}`

## API Endpoints

### Upload Drawing
```
POST /api/projects/{project_id}/drawings
- file: PDF file
- drawing_type: "architectural" | "engineering"
- drawing_date: "YYYY-MM-DD"
- architect_name: "Architect Name" (required for architectural)
- engineer_name: "Engineer Name" (required for engineering)
- revision_number: "Rev 1" (optional)
- notes: "Any notes" (optional)
```

### Update Drawing Metadata
```
PATCH /api/drawings/{drawing_id}
- drawing_date: "YYYY-MM-DD"
- architect_name: "New Architect"
- engineer_name: "New Engineer"
- revision_number: "Rev 2"
```

### Get Project Drawings
```
GET /api/projects/{project_id}/drawings
Returns all drawings for the project
```

## Database Behavior

The `drawings` table has a trigger that:
- When a new architectural drawing is uploaded with `is_current = TRUE`:
  - Updates `projects.drawings_date` to the new drawing date
  - Updates `projects.architect` to the architect name (if provided)
  - Marks other architectural drawings as `is_current = FALSE`

- When a new engineering drawing is uploaded with `is_current = TRUE`:
  - Updates `projects.engineering_date` to the new drawing date
  - Updates `projects.engineer` to the engineer name (if provided)
  - Marks other engineering drawings as `is_current = FALSE`

## Frontend UI Needed

### Drawing Upload Form
- File upload button
- Drawing type dropdown (Architectural / Engineering)
- Date picker
- Architect name field (shown for architectural)
- Engineer name field (shown for engineering)
- Revision number field (optional)
- Notes field (optional)
- Submit button

### Drawing List View
- Show all drawings for project
- Columns: Type, Date, Architect/Engineer, Revision, Actions
- "Edit" button to update metadata
- "Upload New Revision" button

### Drawing Edit Form
- Date picker (pre-filled)
- Architect/Engineer name (pre-filled)
- Revision number (pre-filled)
- Save button

## Benefits

1. **Automatic Updates** - Project dates update automatically
2. **Contract Generation** - Template filler uses latest dates
3. **Revision Tracking** - Keep history of all drawing versions
4. **Simple** - No complex schedule extraction, just metadata
5. **Future Ready** - Can add schedule extraction later if needed

---

**Focus: Store drawings and metadata for contract generation. Keep it simple!** ✅

