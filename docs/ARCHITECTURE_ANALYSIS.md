# Architecture Analysis & Recommendations

## Current Architecture

### What We Have:
1. **Frontend** → Direct Supabase calls for basic CRUD (projects, subcontracts)
2. **Backend** → FastAPI handles complex operations (proposals, AI, Word generation)
3. **Database** → Supabase PostgreSQL

### Current API Endpoints:
- ✅ `POST /api/projects/{project_id}/drawings` - Upload drawing
- ✅ `POST /api/projects/{project_id}/proposals` - Upload proposal
- ✅ `GET /api/projects/{project_id}/drawings` - Get drawings
- ✅ `PATCH /api/drawings/{drawing_id}` - Update drawing
- ✅ `GET /api/subcontracts/{subcontract_id}/download-contract` - Download Word doc
- ✅ `POST /api/subcontracts/{subcontract_id}/generate-contract` - Generate contract HTML

### What's Missing:

#### 1. **Full CRUD API for All Tables**
- Projects: GET, POST, PUT, DELETE
- Subcontracts: GET, POST, PUT, DELETE
- Change Orders: GET, POST, PUT, DELETE
- Invoices: GET, POST, PUT, DELETE
- Payments: GET, POST, PUT, DELETE
- Scope Items: GET, POST, PUT, DELETE

#### 2. **Security & Authentication**
- Row Level Security (RLS) policies in Supabase
- Authentication middleware
- User management

#### 3. **File Storage**
- Supabase Storage integration for drawings/files
- File upload/download endpoints

#### 4. **Business Logic Endpoints**
- Update subcontract amounts (change orders)
- Calculate totals and percentages
- Invoice processing
- Payment tracking

## Do You Need Edge Functions?

**Short Answer: NO, not for basic operations**

### Edge Functions Are Useful For:
- Background jobs (sending emails, notifications)
- Scheduled tasks (daily reports, cleanup)
- Webhooks (third-party integrations)
- Complex serverless operations

### Edge Functions Are NOT Needed For:
- Basic CRUD operations (use FastAPI backend)
- File uploads (use Supabase Storage + FastAPI)
- Database queries (use Supabase client or FastAPI)
- Business logic (use FastAPI backend)

## Recommended Architecture

```
Frontend (React)
    ↓
    ├─→ Supabase Client (for simple reads with RLS)
    └─→ FastAPI Backend (for complex operations, writes, business logic)
            ↓
        Supabase Database
```

### When to Use Each:

**Use Supabase Client Directly:**
- Simple SELECT queries
- Real-time subscriptions
- When RLS policies handle security

**Use FastAPI Backend:**
- Complex business logic
- File processing (PDFs, Word docs)
- AI operations
- Data validation
- Calculations
- All write operations (for consistency)

## Next Steps

1. ✅ Add full CRUD endpoints for all tables
2. ✅ Add Supabase Storage integration
3. ✅ Add Row Level Security policies
4. ✅ Add authentication
5. ⚠️ Consider Edge Functions only if you need:
   - Scheduled tasks
   - Background jobs
   - Webhooks

