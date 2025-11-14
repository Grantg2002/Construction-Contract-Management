# Drawing Schedule Extraction Plan

## Overview
Extract structured data from architectural drawings (door schedules, window schedules, finish schedules) using AI, then store with project for reference and estimating.

## What We'll Extract

### 1. Door Schedules
- Door type/designation (e.g., "101", "102A")
- Door type (e.g., "Wood", "Metal", "Hollow Metal")
- Size (e.g., "3-0 x 7-0")
- Frame type
- Hardware set
- Quantity
- Location/room

### 2. Window Schedules
- Window type/designation
- Window type (e.g., "Fixed", "Casement", "Double-Hung")
- Size
- Glazing type
- Quantity
- Location

### 3. Finish Schedules
- **Floors:**
  - Room/Area
  - Finish type (e.g., "VCT", "Carpet", "Tile")
  - Square footage
  
- **Ceilings:**
  - Room/Area
  - Finish type (e.g., "Acoustic Tile", "Gypsum Board")
  - Square footage
  
- **Paint:**
  - Room/Area
  - Paint type/finish
  - Square footage

## Database Schema

### New Table: `drawing_schedules`
Stores extracted schedule data from drawings.

```sql
CREATE TABLE drawing_schedules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  drawing_id UUID REFERENCES drawings(id) ON DELETE CASCADE,
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  
  -- Schedule Type
  schedule_type TEXT NOT NULL, -- 'door', 'window', 'floor', 'ceiling', 'paint'
  
  -- Item Details
  item_designation TEXT, -- e.g., "101", "W1", "Room 101"
  item_type TEXT, -- e.g., "Wood Door", "Fixed Window", "VCT"
  size TEXT, -- e.g., "3-0 x 7-0", "4-0 x 5-0"
  quantity INTEGER DEFAULT 1,
  
  -- Additional Details (JSON for flexibility)
  details JSONB, -- Hardware sets, glazing types, finish specs, etc.
  
  -- Location
  location TEXT, -- Room name or area
  
  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Workflow

### 1. Upload Drawing
- User uploads architectural/engineering drawing PDF
- User enters: drawing date, architect/engineer name, revision
- Option: "Extract schedules?" checkbox

### 2. AI Extraction (if enabled)
- Extract text from PDF
- Send to GPT-4o with prompt to extract schedules
- Parse structured data
- Store in `drawing_schedules` table

### 3. Manual Review/Edit
- User can view extracted schedules
- Edit quantities, types, etc.
- Add missing items manually

### 4. Use in Contracts
- When creating subcontracts, reference schedule data
- "This project has 15 wood doors, 8 metal doors..."
- Helps verify scope completeness

## API Endpoints

### Upload Drawing with Schedule Extraction
```
POST /api/projects/{project_id}/drawings
- file: PDF
- drawing_type: "architectural" | "engineering"
- drawing_date: YYYY-MM-DD
- architect_name: string (optional)
- engineer_name: string (optional)
- extract_schedules: boolean (default: false)
```

### Get Drawing Schedules
```
GET /api/drawings/{drawing_id}/schedules
GET /api/projects/{project_id}/schedules
```

### Update Drawing Metadata
```
PATCH /api/drawings/{drawing_id}
- drawing_date: YYYY-MM-DD
- architect_name: string
- engineer_name: string
- revision_number: string
```

### Update Schedule Item
```
PATCH /api/schedules/{schedule_id}
- quantity: integer
- item_type: string
- etc.
```

## AI Extraction Prompt

```
You are analyzing architectural drawing schedules. Extract structured data from:

1. DOOR SCHEDULES:
   - Find door schedule table/section
   - Extract: door designation, type, size, frame, hardware, quantity, location

2. WINDOW SCHEDULES:
   - Find window schedule table/section
   - Extract: window designation, type, size, glazing, quantity, location

3. FINISH SCHEDULES:
   - Find finish schedule (floors, ceilings, paint)
   - Extract: room/area, finish type, square footage

Return JSON with this structure:
{
  "doors": [
    {
      "designation": "101",
      "type": "Wood Door",
      "size": "3-0 x 7-0",
      "frame": "Hollow Metal Frame",
      "hardware": "H1",
      "quantity": 1,
      "location": "Office 101"
    }
  ],
  "windows": [...],
  "floors": [...],
  "ceilings": [...],
  "paint": [...]
}
```

## Frontend UI

### Drawing Upload Form
- File upload
- Drawing type dropdown
- Date picker
- Architect/Engineer name fields
- "Extract schedules?" checkbox
- Revision number

### Drawing Management Page
- List all drawings for project
- Show drawing date, architect, revision
- "Edit" button to update metadata
- "View Schedules" button

### Schedule View/Edit
- Tables for each schedule type
- Editable quantities/types
- Add/delete items
- Export to CSV/Excel

## Benefits

1. **Automated Data Entry** - No manual typing of schedules
2. **Scope Verification** - Compare subcontractor proposals to schedules
3. **Historical Reference** - "Last project had 20 doors, this one has 15"
4. **Estimating** - Use schedule data for future estimates
5. **Change Tracking** - Track revisions and changes

## Implementation Steps

1. ✅ Create `drawing_schedules` table migration
2. ✅ Add AI extraction function for schedules
3. ✅ Update drawing upload endpoint to support extraction
4. ✅ Create schedule management endpoints
5. ✅ Build frontend UI for drawing management
6. ✅ Build schedule view/edit UI

---

**This will save tons of time and improve accuracy!** 🚀

