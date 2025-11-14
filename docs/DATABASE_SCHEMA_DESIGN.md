# Database Schema Design - Contract Tracking System

## Overview

This schema supports comprehensive tracking of:
- Projects and project details
- Subcontracts with full scope breakdown
- Change orders (cost modifications)
- Invoices and payment applications
- Progress tracking (billed vs completed)
- Historical cost data for estimating

---

## Core Tables

### 1. `projects` - Enhanced Project Information

```sql
CREATE TABLE IF NOT EXISTS projects (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  
  -- Basic Info
  name TEXT NOT NULL,
  description TEXT,
  
  -- Project Address
  street TEXT,
  city TEXT,
  state TEXT,
  zip TEXT,
  
  -- Project Team
  engineer TEXT,
  architect TEXT,
  pm_name TEXT,
  pm_phone TEXT,
  
  -- Drawing Information
  drawings_date DATE,
  engineering_date DATE,
  
  -- Project Financials
  total_budget DECIMAL(12, 2),
  current_spent DECIMAL(12, 2),
  
  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  project_start_date DATE,
  project_end_date DATE,
  
  -- Status
  status TEXT DEFAULT 'active', -- active, completed, on_hold, cancelled
  project_number TEXT UNIQUE
);
```

**Placeholders Supported:**
- `{{project.name}}`
- `{{project.street}}`
- `{{project.city}}`
- `{{project.state}}`
- `{{project.zip}}`
- `{{engineer}}`
- `{{architect}}`
- `{{pm.name}}`
- `{{pm.number}}`
- `{{drawings.date}}`
- `{{engineering.date}}`

---

### 2. `subcontracts` - Main Subcontract Table

```sql
CREATE TABLE IF NOT EXISTS subcontracts (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  
  -- Subcontractor Information
  company_name TEXT NOT NULL,
  representative_name TEXT,
  street TEXT,
  city TEXT,
  state TEXT,
  zip TEXT,
  email TEXT,
  phone TEXT,
  fax TEXT,
  
  -- Contract Details
  contract_number TEXT UNIQUE,
  original_amount DECIMAL(12, 2) NOT NULL,
  current_amount DECIMAL(12, 2) NOT NULL, -- Updated by change orders
  proposal_date DATE,
  contract_date DATE,
  
  -- Scope Information
  scope_of_work_html TEXT, -- Full scope description
  scope_summary TEXT, -- Short summary
  
  -- Drawing Requirements
  drawings_required BOOLEAN DEFAULT FALSE,
  as_built_required BOOLEAN DEFAULT FALSE,
  
  -- Status Tracking
  status TEXT DEFAULT 'draft', -- draft, active, completed, cancelled
  percentage_complete DECIMAL(5, 2) DEFAULT 0, -- 0-100
  total_billed DECIMAL(12, 2) DEFAULT 0,
  total_paid DECIMAL(12, 2) DEFAULT 0,
  remaining_balance DECIMAL(12, 2), -- Calculated: current_amount - total_paid
  
  -- Progress Tracking
  last_invoice_date DATE,
  last_payment_date DATE,
  
  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  -- Metadata
  notes TEXT,
  contract_file_url TEXT -- Link to generated contract document
);
```

**Placeholders Supported:**
- `{{sub.company}}`
- `{{sub.rep}}`
- `{{sub.street}}`
- `{{sub.city}}`
- `{{sub.state}}`
- `{{sub.zip}}`
- `{{sub.email}}`
- `{{sub.phone}}`
- `{{sub.fax}}`
- `{{proposal.date}}`
- `{{proposal.pricing}}`
- `{{scope.html}}`
- `{{dwg.req}}` / `{{dwg.not_req}}`
- `{{AB.req}}`

---

### 3. `subcontract_line_items` - Detailed Scope Breakdown

```sql
CREATE TABLE IF NOT EXISTS subcontract_line_items (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  subcontract_id UUID REFERENCES subcontracts(id) ON DELETE CASCADE,
  
  -- Line Item Details
  item_number INTEGER NOT NULL,
  description TEXT NOT NULL,
  quantity DECIMAL(10, 2),
  unit TEXT, -- e.g., "SF", "LF", "EA", "HR"
  unit_price DECIMAL(10, 2),
  line_total DECIMAL(12, 2) NOT NULL, -- quantity * unit_price
  
  -- Work Category (for historical tracking)
  work_category TEXT, -- e.g., "Electrical", "Plumbing", "HVAC", "Framing"
  work_type TEXT, -- e.g., "Install", "Remove", "Repair"
  
  -- Progress Tracking
  quantity_completed DECIMAL(10, 2) DEFAULT 0,
  amount_billed DECIMAL(12, 2) DEFAULT 0,
  amount_paid DECIMAL(12, 2) DEFAULT 0,
  
  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  -- Ordering
  display_order INTEGER DEFAULT 0,
  
  CONSTRAINT unique_item_per_subcontract UNIQUE (subcontract_id, item_number)
);
```

**Purpose:** 
- Track individual scope items
- Calculate costs per work type
- Build historical cost database
- Match invoices to specific line items

---

### 4. `change_orders` - Contract Modifications

```sql
CREATE TABLE IF NOT EXISTS change_orders (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  subcontract_id UUID REFERENCES subcontracts(id) ON DELETE CASCADE,
  
  -- Change Order Details
  change_order_number TEXT NOT NULL,
  description TEXT NOT NULL,
  reason TEXT, -- Why the change was needed
  
  -- Financial Impact
  amount_change DECIMAL(12, 2) NOT NULL, -- Can be positive or negative
  previous_amount DECIMAL(12, 2) NOT NULL,
  new_amount DECIMAL(12, 2) NOT NULL,
  
  -- Approval
  status TEXT DEFAULT 'pending', -- pending, approved, rejected
  approved_by TEXT,
  approved_date DATE,
  
  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  change_order_date DATE DEFAULT CURRENT_DATE,
  
  -- Metadata
  notes TEXT,
  attachment_url TEXT -- Link to change order document
);

-- Trigger to update subcontract.current_amount when change order is approved
CREATE OR REPLACE FUNCTION update_subcontract_amount()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.status = 'approved' AND OLD.status != 'approved' THEN
    UPDATE subcontracts 
    SET current_amount = NEW.new_amount,
        updated_at = NOW()
    WHERE id = NEW.subcontract_id;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER change_order_approved
AFTER UPDATE ON change_orders
FOR EACH ROW
EXECUTE FUNCTION update_subcontract_amount();
```

**Purpose:**
- Track all cost modifications
- Maintain audit trail
- Calculate final contract amount

---

### 5. `invoices` - Subcontractor Invoices

```sql
CREATE TABLE IF NOT EXISTS invoices (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  subcontract_id UUID REFERENCES subcontracts(id) ON DELETE CASCADE,
  
  -- Invoice Details
  invoice_number TEXT NOT NULL,
  invoice_date DATE NOT NULL,
  due_date DATE,
  
  -- Financials
  invoice_amount DECIMAL(12, 2) NOT NULL,
  amount_paid DECIMAL(12, 2) DEFAULT 0,
  amount_remaining DECIMAL(12, 2), -- Calculated: invoice_amount - amount_paid
  
  -- Billing Period
  period_start DATE,
  period_end DATE,
  
  -- Progress Claims
  work_completed_percentage DECIMAL(5, 2), -- What % of work they claim is done
  materials_supplied_percentage DECIMAL(5, 2),
  
  -- Status
  status TEXT DEFAULT 'pending', -- pending, approved, paid, disputed, rejected
  payment_date DATE,
  
  -- Matching to Contract
  matches_contract_scope BOOLEAN, -- Does invoice align with contract?
  variance_notes TEXT, -- If there's a discrepancy, note it
  
  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  -- File Storage
  invoice_file_url TEXT, -- Link to uploaded invoice PDF/image
  ocr_text TEXT, -- Extracted text from invoice (for future automation)
  
  -- Metadata
  notes TEXT,
  
  CONSTRAINT unique_invoice_number UNIQUE (subcontract_id, invoice_number)
);
```

**Purpose:**
- Track all invoices
- Match invoices to contract scope
- Flag discrepancies
- Calculate remaining balance

---

### 6. `invoice_line_items` - Invoice Detail Breakdown

```sql
CREATE TABLE IF NOT EXISTS invoice_line_items (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  invoice_id UUID REFERENCES invoices(id) ON DELETE CASCADE,
  subcontract_line_item_id UUID REFERENCES subcontract_line_items(id) ON DELETE SET NULL,
  
  -- Line Item Details
  description TEXT NOT NULL,
  quantity DECIMAL(10, 2),
  unit TEXT,
  unit_price DECIMAL(10, 2),
  line_total DECIMAL(12, 2) NOT NULL,
  
  -- Matching
  matches_contract_item BOOLEAN DEFAULT FALSE,
  variance_amount DECIMAL(12, 2), -- Difference from contract item
  
  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

**Purpose:**
- Break down invoices by line item
- Match invoice items to contract items
- Identify discrepancies at item level

---

### 7. `payments` - Payment Tracking

```sql
CREATE TABLE IF NOT EXISTS payments (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  invoice_id UUID REFERENCES invoices(id) ON DELETE CASCADE,
  subcontract_id UUID REFERENCES subcontracts(id) ON DELETE CASCADE,
  
  -- Payment Details
  payment_number TEXT NOT NULL,
  payment_date DATE NOT NULL,
  payment_amount DECIMAL(12, 2) NOT NULL,
  payment_method TEXT, -- check, wire, ach, etc.
  check_number TEXT,
  
  -- Status
  status TEXT DEFAULT 'pending', -- pending, processed, cleared, voided
  
  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  -- Metadata
  notes TEXT,
  payment_file_url TEXT -- Link to payment confirmation
);

-- Trigger to update invoice and subcontract amounts when payment is processed
CREATE OR REPLACE FUNCTION update_payment_amounts()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.status = 'processed' AND OLD.status != 'processed' THEN
    -- Update invoice
    UPDATE invoices 
    SET amount_paid = COALESCE(amount_paid, 0) + NEW.payment_amount,
        amount_remaining = invoice_amount - (COALESCE(amount_paid, 0) + NEW.payment_amount),
        updated_at = NOW()
    WHERE id = NEW.invoice_id;
    
    -- Update subcontract
    UPDATE subcontracts 
    SET total_paid = COALESCE(total_paid, 0) + NEW.payment_amount,
        remaining_balance = current_amount - (COALESCE(total_paid, 0) + NEW.payment_amount),
        last_payment_date = NEW.payment_date,
        updated_at = NOW()
    WHERE id = NEW.subcontract_id;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER payment_processed
AFTER UPDATE ON payments
FOR EACH ROW
EXECUTE FUNCTION update_payment_amounts();
```

---

### 8. `historical_cost_data` - For Future Estimating

```sql
CREATE TABLE IF NOT EXISTS historical_cost_data (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  
  -- Work Classification
  work_category TEXT NOT NULL, -- e.g., "Electrical", "Plumbing"
  work_type TEXT NOT NULL, -- e.g., "Install Outlets", "Run Conduit"
  unit TEXT NOT NULL, -- e.g., "SF", "LF", "EA"
  
  -- Cost Data
  unit_price DECIMAL(10, 2) NOT NULL,
  project_location TEXT, -- City/State for regional pricing
  project_year INTEGER, -- For inflation tracking
  
  -- Source
  source_subcontract_id UUID REFERENCES subcontracts(id) ON DELETE SET NULL,
  source_line_item_id UUID REFERENCES subcontract_line_items(id) ON DELETE SET NULL,
  
  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  -- Metadata
  notes TEXT
);

-- Index for fast lookups
CREATE INDEX idx_historical_cost_lookup 
ON historical_cost_data(work_category, work_type, unit, project_location);
```

**Purpose:**
- Build historical cost database
- Use for future project estimates
- Track cost trends over time

---

## Calculated Fields & Views

### View: `subcontract_summary`

```sql
CREATE OR REPLACE VIEW subcontract_summary AS
SELECT 
  s.id,
  s.contract_number,
  s.company_name,
  p.name as project_name,
  s.original_amount,
  s.current_amount,
  COALESCE(SUM(co.amount_change), 0) as total_change_orders,
  s.total_billed,
  s.total_paid,
  s.remaining_balance,
  s.percentage_complete,
  COUNT(DISTINCT i.id) as invoice_count,
  COUNT(DISTINCT p.id) as payment_count,
  s.status
FROM subcontracts s
LEFT JOIN projects p ON s.project_id = p.id
LEFT JOIN change_orders co ON s.id = co.subcontract_id AND co.status = 'approved'
LEFT JOIN invoices i ON s.id = i.subcontract_id
LEFT JOIN payments p ON s.id = p.subcontract_id
GROUP BY s.id, p.name;
```

---

## Additional Tracking Fields to Consider

### For Projects:
- `owner_name` - Project owner
- `owner_contact` - Owner phone/email
- `permit_number` - Building permit number
- `insurance_required` - Insurance requirements

### For Subcontracts:
- `warranty_period` - Warranty duration
- `start_date` - Work start date
- `completion_date` - Expected completion date
- `actual_completion_date` - When work actually finished
- `retainage_percentage` - Retainage amount
- `insurance_certificate_url` - Link to insurance cert

### For Invoices:
- `retainage_amount` - Retainage held
- `previous_retainage_released` - Retainage released this period
- `lien_waiver_received` - Lien waiver status

---

## Indexes for Performance

```sql
-- Common queries
CREATE INDEX idx_subcontracts_project ON subcontracts(project_id);
CREATE INDEX idx_subcontracts_status ON subcontracts(status);
CREATE INDEX idx_invoices_subcontract ON invoices(subcontract_id);
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_change_orders_subcontract ON change_orders(subcontract_id);
CREATE INDEX idx_line_items_subcontract ON subcontract_line_items(subcontract_id);
CREATE INDEX idx_payments_invoice ON payments(invoice_id);
```

---

## Next Steps

1. **Review this schema** - Does it cover all your tracking needs?
2. **Provide Supabase credentials** - I'll inspect your current schema
3. **Create migration script** - Align your database with this design
4. **Build frontend** - Forms to input/manage all this data
5. **Add reporting** - Views and reports for analytics

