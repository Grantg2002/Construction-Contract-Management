# Full Stack Testing Guide

## Quick Start

### 1. Start Backend Server
```bash
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The backend will be available at: http://localhost:8000
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### 2. Start Frontend Server
```bash
cd frontend
npm run dev
```

The frontend will be available at: http://localhost:5173

## Testing Workflow

### Step 1: Create a Project
1. Open http://localhost:5173 in your browser
2. Click "New Project" button
3. Fill in:
   - Project Name (required)
   - Project Start Date (optional)
   - Location (optional)
4. Optionally upload files:
   - Drawings (PDF, DWG)
   - Permits & Approvals (PDF)
   - Reference Docs (PDF, DOC, DOCX)
5. Click "Create Project"

**Expected Result:** Project appears in the dashboard grid

### Step 2: Upload Drawings (Optional)
1. Click on a project to open it
2. Click "Files" button in the project header
3. Upload architectural or engineering drawings
4. Fill in required metadata:
   - Drawing Type (architectural/engineering)
   - Drawing Date
   - Architect Name (for architectural)
   - Engineer Name (for engineering)

**Expected Result:** Drawing is stored and linked to project

### Step 3: Upload a Proposal
1. From the project detail page, click "Upload Proposals"
2. Select a PDF proposal file
3. Click "Upload and Analyze"

**Expected Result:** 
- Proposal is processed by AI
- Company name, price, date, and scope are extracted
- A new subcontract is created in the database
- You're redirected back to the project page
- The subcontract appears in the subcontracts table

### Step 4: View Subcontract Details
1. On the project detail page, find your subcontract in the table
2. Click on the "Trade / Scope" cell to view full scope HTML
3. Check the progress bar showing % billed

**Expected Result:** 
- Modal opens showing formatted scope of work
- Progress bar shows 0% (no invoices yet)

## Available API Endpoints

### Projects
- `POST /api/projects/{project_id}/drawings` - Upload drawing
- `POST /api/projects/{project_id}/proposals` - Upload proposal
- `GET /api/projects/{project_id}/drawings` - Get all drawings for project
- `GET /api/projects/{project_id}/schedules` - Get drawing schedules

### Drawings
- `PATCH /api/drawings/{drawing_id}` - Update drawing metadata
- `GET /api/drawings/{drawing_id}/schedules` - Get schedules from drawing

### Subcontracts
- `POST /api/subcontracts/{subcontract_id}/generate-contract` - Generate contract HTML

## Troubleshooting

### Backend not starting?
- Check that `.env` file exists in `backend/` directory
- Verify `SUPABASE_URL` and `SUPABASE_ANON_KEY` are set
- Check that `OPENAI_API_KEY` is set (for proposal processing)
- Install dependencies: `pip install -r requirements.txt`

### Frontend not connecting to backend?
- Make sure backend is running on port 8000
- Check browser console (F12) for CORS errors
- Verify Vite proxy is configured in `frontend/vite.config.js`

### Proposal upload failing?
- Check backend logs for errors
- Verify OpenAI API key is valid
- Check that proposal file is PDF or DOCX format
- Ensure project ID is valid

### Database errors?
- Verify Supabase credentials in `.env`
- Check that all required tables exist
- Run migrations if needed: `backend/migrations/*.sql`

## Next Steps After Testing

Once everything works:
1. ✅ Test full workflow end-to-end
2. ✅ Verify data is stored correctly in Supabase
3. ✅ Check that AI extraction is working
4. 🎨 Then we'll improve UI aesthetics

