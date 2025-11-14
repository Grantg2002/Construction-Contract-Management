# Quick Start: Testing the Backend

## Step 1: Install Dependencies

Make sure you have all Python packages installed:

```powershell
cd backend
pip install -r requirements.txt
```

## Step 2: Set Up Environment Variables

Create `backend/.env` file with:

```
OPENAI_API_KEY=your-openai-api-key-here
SUPABASE_URL=https://olesfyxldqbtxofkequi.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9sZXNmeXhsZHFidHhvZmtlcXVpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI5NzA4MzEsImV4cCI6MjA3ODU0NjgzMX0.OD3USP8Z962x45v2OjI8kS_C3M3xOgGN4GnOM502lBA
```

## Step 3: Start the Backend Server

```powershell
cd backend
python -m uvicorn main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

## Step 4: Test the API

### Option A: Use FastAPI Interactive Docs (Easiest!)

1. Open your browser: **http://localhost:8000/docs**
2. Click on `GET /health`
3. Click "Try it out" → "Execute"
4. Should return: `{"status": "healthy"}`

### Option B: Test with curl

```powershell
# Test health endpoint
curl http://localhost:8000/health

# Should return: {"status":"healthy"}
```

## Step 5: Test Drawing Upload

**You'll need:**
- A project ID from your Supabase database
- A PDF file (drawing or any test PDF)

### Using FastAPI Docs:
1. Go to http://localhost:8000/docs
2. Find `POST /api/projects/{project_id}/drawings`
3. Click "Try it out"
4. Enter your project_id
5. Upload a file
6. Fill in:
   - `drawing_type`: `architectural` or `engineering`
   - `drawing_date`: `2025-01-15`
   - `architect_name`: (optional)
   - `engineer_name`: (optional)
7. Click "Execute"

### Using curl:
```powershell
curl -X POST "http://localhost:8000/api/projects/YOUR_PROJECT_ID/drawings" `
  -F "file=@test_drawing.pdf" `
  -F "drawing_type=architectural" `
  -F "drawing_date=2025-01-15"
```

## Step 6: Test Proposal Upload

**You'll need:**
- A project ID
- A proposal PDF (use one of your example proposals!)

### Using FastAPI Docs:
1. Find `POST /api/projects/{project_id}/proposals`
2. Click "Try it out"
3. Enter project_id
4. Upload a proposal PDF
5. Click "Execute"
6. Wait for AI extraction (may take 10-30 seconds)
7. Check the response for:
   - `subcontract_id`
   - `extracted_data` (company name, price, scope items)
   - `extraction_cost`

## Step 7: Test Contract Generation

**You'll need:**
- A subcontract_id from Step 6

### Using FastAPI Docs:
1. Find `POST /api/subcontracts/{subcontract_id}/generate-contract`
2. Click "Try it out"
3. Enter subcontract_id
4. In the Request body, enter JSON:
```json
{
  "company_name": "Test Company",
  "representative_name": "John Doe",
  "street": "123 Main St",
  "city": "Test City",
  "state": "CA",
  "zip": "12345",
  "email": "test@example.com",
  "phone": "555-1234",
  "fax": "555-5678"
}
```
5. Click "Execute"
6. Check response for `contract_html`

## Troubleshooting

### "Module not found"
```powershell
pip install -r requirements.txt
```

### "OPENAI_API_KEY not set"
- Check `backend/.env` file exists
- Make sure it has `OPENAI_API_KEY=...`

### "Connection refused"
- Make sure backend is running: `python -m uvicorn main:app --reload`
- Check it's running on port 8000

### "Table 'drawings' does not exist"
- Run the migration: `003_create_drawings_table_FIXED.sql` in Supabase SQL Editor

### "No project found"
- Create a project in Supabase first, or use an existing project ID

## Next Steps

Once testing works:
1. ✅ Test drawing upload
2. ✅ Test proposal upload and extraction
3. ✅ Test contract generation
4. ✅ Verify data in Supabase dashboard

Then we can build the frontend! 🚀

