# Testing the Backend Without a Frontend

There are **3 easy ways** to test the backend API:

---

## Method 1: FastAPI Interactive Docs (Easiest! 🎉)

FastAPI automatically generates interactive API documentation!

### Steps:

1. **Start the backend server:**
   ```bash
   cd backend
   python -m uvicorn main:app --reload
   ```

2. **Open your browser:**
   - Go to: **http://localhost:8000/docs**
   - This is the **Swagger UI** - interactive API documentation!

3. **Test endpoints:**
   - Click on any endpoint (e.g., `POST /api/projects/{project_id}/drawings`)
   - Click "Try it out"
   - Fill in the parameters
   - Upload files using the file picker
   - Click "Execute"
   - See the response!

**Alternative:** Go to **http://localhost:8000/redoc** for ReDoc format (cleaner, read-only)

---

## Method 2: Using curl (Command Line)

### Test Health Check:
```bash
curl http://localhost:8000/health
```

### Test Drawing Upload:
```bash
curl -X POST "http://localhost:8000/api/projects/YOUR_PROJECT_ID/drawings" \
  -F "file=@path/to/drawing.pdf" \
  -F "drawing_type=architectural" \
  -F "drawing_date=2025-01-15" \
  -F "architect_name=John Architect"
```

### Test Proposal Upload:
```bash
curl -X POST "http://localhost:8000/api/projects/YOUR_PROJECT_ID/proposals" \
  -F "file=@path/to/proposal.pdf"
```

### Test Contract Generation:
```bash
curl -X POST "http://localhost:8000/api/subcontracts/YOUR_SUBCONTRACT_ID/generate-contract" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Test Company",
    "representative_name": "John Doe",
    "street": "123 Main St",
    "city": "Test City",
    "state": "CA",
    "zip": "12345",
    "email": "test@example.com",
    "phone": "555-1234",
    "fax": "555-5678"
  }'
```

---

## Method 3: Python Test Script

I've created `backend/test_api.py` for you!

### Steps:

1. **Install requests** (if not already installed):
   ```bash
   pip install requests
   ```

2. **Edit the script** to add your project ID and file paths:
   ```python
   PROJECT_ID = "your-project-uuid-here"
   ```

3. **Run the script:**
   ```bash
   cd backend
   python test_api.py
   ```

---

## Quick Start Guide

### 1. First, get a Project ID

You need a project in your Supabase database first. You can:
- Create one manually in Supabase dashboard
- Or use the frontend (when built)
- Or create one via API:

```bash
# Create a test project (if you have a projects endpoint)
curl -X POST "http://localhost:8000/api/projects" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Project",
    "description": "Testing the API"
  }'
```

### 2. Test Drawing Upload

```bash
curl -X POST "http://localhost:8000/api/projects/YOUR_PROJECT_ID/drawings" \
  -F "file=@test_drawing.pdf" \
  -F "drawing_type=architectural" \
  -F "drawing_date=2025-01-15"
```

### 3. Test Proposal Upload

```bash
curl -X POST "http://localhost:8000/api/projects/YOUR_PROJECT_ID/proposals" \
  -F "file=@example_proposal.pdf"
```

This will:
- Extract text from PDF
- Use AI to extract structured data
- Store in database
- Return extracted data + scope HTML

### 4. Test Contract Generation

After uploading a proposal, you'll get a `subcontract_id`. Use it to generate a contract:

```bash
curl -X POST "http://localhost:8000/api/subcontracts/YOUR_SUBCONTRACT_ID/generate-contract" \
  -H "Content-Type: application/json" \
  -d @subcontractor_data.json
```

---

## Expected Responses

### Drawing Upload Success:
```json
{
  "success": true,
  "drawing_id": "uuid-here",
  "message": "Drawing uploaded successfully"
}
```

### Proposal Upload Success:
```json
{
  "success": true,
  "subcontract_id": "uuid-here",
  "extracted_data": {
    "company_name": "HALYARD",
    "proposal_date": "2025-01-15",
    "total_price": 114120.00,
    "scope_items": [...],
    "excluded_items": [...]
  },
  "scope_html": "<div>...</div>",
  "extraction_cost": 0.0123
}
```

### Contract Generation Success:
```json
{
  "success": true,
  "contract_html": "<html>...</html>"
}
```

The contract HTML will be saved to `backend/test_contract_output.html` if you use the test script.

---

## Troubleshooting

### "Connection refused"
- Make sure backend is running: `python -m uvicorn main:app --reload`

### "Module not found"
- Install dependencies: `pip install -r backend/requirements.txt`

### "OPENAI_API_KEY not set"
- Create `backend/.env` file with:
  ```
  OPENAI_API_KEY=your-key-here
  SUPABASE_URL=your-url
  SUPABASE_KEY=your-key
  ```

### "Table 'drawings' does not exist"
- Run the migration: `backend/migrations/003_create_drawings_table.sql` in Supabase SQL Editor

---

## Recommended: Use FastAPI Docs!

**http://localhost:8000/docs** is the easiest way to test everything interactively! 🚀

