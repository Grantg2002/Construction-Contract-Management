# Complete Backend API Reference

## Overview
The backend now provides full CRUD operations for all database tables, plus specialized endpoints for complex operations.

## Base URL
- Development: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

## API Endpoints

### Projects

#### Get All Projects
```
GET /api/projects?skip=0&limit=100&status=active
```

#### Get Single Project
```
GET /api/projects/{project_id}
```

#### Update Project
```
PUT /api/projects/{project_id}
Body: { "name": "...", "status": "...", ... }
```

#### Delete Project
```
DELETE /api/projects/{project_id}
```

### Subcontracts

#### Get All Subcontracts for Project
```
GET /api/projects/{project_id}/subcontracts
```

#### Get Single Subcontract
```
GET /api/subcontracts/{subcontract_id}
```

#### Update Subcontract
```
PUT /api/subcontracts/{subcontract_id}
Body: { "current_amount": 150000, "status": "active", ... }
```

#### Delete Subcontract
```
DELETE /api/subcontracts/{subcontract_id}
```

### Scope Items

#### Get All Scope Items
```
GET /api/subcontracts/{subcontract_id}/scope-items
```

#### Create Scope Item
```
POST /api/subcontracts/{subcontract_id}/scope-items
Body: {
  "category": "Framing",
  "description": "...",
  "quantity": 1000,
  "unit": "SF",
  "unit_price": 5.50,
  "line_total": 5500,
  "is_included": true
}
```

#### Update Scope Item
```
PUT /api/scope-items/{scope_item_id}
Body: { "description": "...", "quantity": 1200, ... }
```

#### Delete Scope Item
```
DELETE /api/scope-items/{scope_item_id}
```

### Change Orders

#### Get All Change Orders
```
GET /api/subcontracts/{subcontract_id}/change-orders
```

#### Create Change Order
```
POST /api/subcontracts/{subcontract_id}/change-orders
Body: {
  "change_order_number": "CO-001",
  "change_amount": 5000,
  "description": "Additional work",
  "change_order_date": "2025-01-15"
}
```
**Note:** Automatically updates subcontract `current_amount`

### Invoices

#### Get All Invoices
```
GET /api/subcontracts/{subcontract_id}/invoices
```

#### Create Invoice
```
POST /api/subcontracts/{subcontract_id}/invoices
Body: {
  "invoice_number": "INV-001",
  "invoice_amount": 25000,
  "invoice_date": "2025-01-15",
  "status": "pending"
}
```
**Note:** Automatically updates subcontract `total_billed`

### Payments

#### Get All Payments
```
GET /api/invoices/{invoice_id}/payments
```

#### Create Payment
```
POST /api/invoices/{invoice_id}/payments
Body: {
  "payment_amount": 25000,
  "payment_date": "2025-01-20",
  "payment_method": "check",
  "check_number": "1234"
}
```

### Complex Operations

#### Upload Proposal
```
POST /api/projects/{project_id}/proposals
Content-Type: multipart/form-data
Body: file (PDF/DOCX)
```

#### Upload Drawing
```
POST /api/projects/{project_id}/drawings
Content-Type: multipart/form-data
Body: 
  - file
  - drawing_type (architectural/engineering)
  - drawing_date
  - architect_name (for architectural)
  - engineer_name (for engineering)
```

#### Download Contract (Word Document)
```
GET /api/subcontracts/{subcontract_id}/download-contract
```

#### Generate Contract HTML
```
POST /api/subcontracts/{subcontract_id}/generate-contract
Body: { "company_name": "...", "street": "...", ... }
```

## Architecture Decision: Edge Functions

**You do NOT need Edge Functions for this application.**

### Current Architecture Works Because:
1. ✅ FastAPI backend handles all business logic
2. ✅ Supabase provides database + storage
3. ✅ Frontend can call Supabase directly for simple reads (with RLS)
4. ✅ Complex operations go through FastAPI backend

### Edge Functions Would Only Be Needed For:
- Scheduled tasks (daily reports, cleanup)
- Background jobs (email notifications)
- Webhooks (third-party integrations)
- Serverless operations that don't need a persistent backend

### Recommended Next Steps:
1. ✅ Add Row Level Security (RLS) policies in Supabase
2. ✅ Add authentication (Supabase Auth)
3. ✅ Add file storage endpoints (Supabase Storage)
4. ⚠️ Consider Edge Functions only if you need scheduled tasks

