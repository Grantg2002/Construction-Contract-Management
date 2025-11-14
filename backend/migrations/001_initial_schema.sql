-- Migration: Initial Schema Setup
-- Run this in your Supabase SQL Editor
-- This creates all tables and columns needed for contract tracking

-- ============================================
-- 1. ENHANCE EXISTING PROJECTS TABLE
-- ============================================
-- Add columns if they don't exist
DO $$ 
BEGIN
    -- Project Address
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='projects' AND column_name='street') THEN
        ALTER TABLE projects ADD COLUMN street TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='projects' AND column_name='city') THEN
        ALTER TABLE projects ADD COLUMN city TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='projects' AND column_name='state') THEN
        ALTER TABLE projects ADD COLUMN state TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='projects' AND column_name='zip') THEN
        ALTER TABLE projects ADD COLUMN zip TEXT;
    END IF;
    
    -- Project Team
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='projects' AND column_name='engineer') THEN
        ALTER TABLE projects ADD COLUMN engineer TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='projects' AND column_name='architect') THEN
        ALTER TABLE projects ADD COLUMN architect TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='projects' AND column_name='pm_name') THEN
        ALTER TABLE projects ADD COLUMN pm_name TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='projects' AND column_name='pm_phone') THEN
        ALTER TABLE projects ADD COLUMN pm_phone TEXT;
    END IF;
    
    -- Drawing Information
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='projects' AND column_name='drawings_date') THEN
        ALTER TABLE projects ADD COLUMN drawings_date DATE;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='projects' AND column_name='engineering_date') THEN
        ALTER TABLE projects ADD COLUMN engineering_date DATE;
    END IF;
    
    -- Project Financials
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='projects' AND column_name='total_budget') THEN
        ALTER TABLE projects ADD COLUMN total_budget DECIMAL(12, 2);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='projects' AND column_name='current_spent') THEN
        ALTER TABLE projects ADD COLUMN current_spent DECIMAL(12, 2);
    END IF;
    
    -- Project Dates
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='projects' AND column_name='project_start_date') THEN
        ALTER TABLE projects ADD COLUMN project_start_date DATE;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='projects' AND column_name='project_end_date') THEN
        ALTER TABLE projects ADD COLUMN project_end_date DATE;
    END IF;
    
    -- Status
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='projects' AND column_name='status') THEN
        ALTER TABLE projects ADD COLUMN status TEXT DEFAULT 'active';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='projects' AND column_name='project_number') THEN
        ALTER TABLE projects ADD COLUMN project_number TEXT UNIQUE;
    END IF;
END $$;

-- ============================================
-- 2. ENHANCE EXISTING SUBCONTRACTS TABLE
-- ============================================
DO $$ 
BEGIN
    -- Subcontractor Information
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='company_name') THEN
        ALTER TABLE subcontracts ADD COLUMN company_name TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='representative_name') THEN
        ALTER TABLE subcontracts ADD COLUMN representative_name TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='street') THEN
        ALTER TABLE subcontracts ADD COLUMN street TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='city') THEN
        ALTER TABLE subcontracts ADD COLUMN city TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='state') THEN
        ALTER TABLE subcontracts ADD COLUMN state TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='zip') THEN
        ALTER TABLE subcontracts ADD COLUMN zip TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='email') THEN
        ALTER TABLE subcontracts ADD COLUMN email TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='phone') THEN
        ALTER TABLE subcontracts ADD COLUMN phone TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='fax') THEN
        ALTER TABLE subcontracts ADD COLUMN fax TEXT;
    END IF;
    
    -- Contract Details
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='contract_number') THEN
        ALTER TABLE subcontracts ADD COLUMN contract_number TEXT UNIQUE;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='original_amount') THEN
        ALTER TABLE subcontracts ADD COLUMN original_amount DECIMAL(12, 2);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='current_amount') THEN
        ALTER TABLE subcontracts ADD COLUMN current_amount DECIMAL(12, 2);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='proposal_date') THEN
        ALTER TABLE subcontracts ADD COLUMN proposal_date DATE;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='contract_date') THEN
        ALTER TABLE subcontracts ADD COLUMN contract_date DATE;
    END IF;
    
    -- Scope Information
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='scope_of_work_html') THEN
        ALTER TABLE subcontracts ADD COLUMN scope_of_work_html TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='scope_summary') THEN
        ALTER TABLE subcontracts ADD COLUMN scope_summary TEXT;
    END IF;
    
    -- Drawing Requirements
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='drawings_required') THEN
        ALTER TABLE subcontracts ADD COLUMN drawings_required BOOLEAN DEFAULT FALSE;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='as_built_required') THEN
        ALTER TABLE subcontracts ADD COLUMN as_built_required BOOLEAN DEFAULT FALSE;
    END IF;
    
    -- Status Tracking
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='status') THEN
        ALTER TABLE subcontracts ADD COLUMN status TEXT DEFAULT 'draft';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='percentage_complete') THEN
        ALTER TABLE subcontracts ADD COLUMN percentage_complete DECIMAL(5, 2) DEFAULT 0;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='total_billed') THEN
        ALTER TABLE subcontracts ADD COLUMN total_billed DECIMAL(12, 2) DEFAULT 0;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='total_paid') THEN
        ALTER TABLE subcontracts ADD COLUMN total_paid DECIMAL(12, 2) DEFAULT 0;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='remaining_balance') THEN
        ALTER TABLE subcontracts ADD COLUMN remaining_balance DECIMAL(12, 2);
    END IF;
    
    -- Progress Tracking
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='last_invoice_date') THEN
        ALTER TABLE subcontracts ADD COLUMN last_invoice_date DATE;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='last_payment_date') THEN
        ALTER TABLE subcontracts ADD COLUMN last_payment_date DATE;
    END IF;
    
    -- Metadata
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='notes') THEN
        ALTER TABLE subcontracts ADD COLUMN notes TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='subcontracts' AND column_name='contract_file_url') THEN
        ALTER TABLE subcontracts ADD COLUMN contract_file_url TEXT;
    END IF;
END $$;

-- ============================================
-- 3. CREATE SUBCONTRACT LINE ITEMS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS subcontract_line_items (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  subcontract_id UUID REFERENCES subcontracts(id) ON DELETE CASCADE,
  
  -- Line Item Details
  item_number INTEGER NOT NULL,
  description TEXT NOT NULL,
  quantity DECIMAL(10, 2),
  unit TEXT,
  unit_price DECIMAL(10, 2),
  line_total DECIMAL(12, 2) NOT NULL,
  
  -- Work Category (for historical tracking)
  work_category TEXT,
  work_type TEXT,
  
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

-- ============================================
-- 4. ENHANCE EXISTING CHANGE ORDERS TABLE
-- ============================================
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='change_orders' AND column_name='change_order_number') THEN
        ALTER TABLE change_orders ADD COLUMN change_order_number TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='change_orders' AND column_name='reason') THEN
        ALTER TABLE change_orders ADD COLUMN reason TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='change_orders' AND column_name='amount_change') THEN
        ALTER TABLE change_orders ADD COLUMN amount_change DECIMAL(12, 2);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='change_orders' AND column_name='previous_amount') THEN
        ALTER TABLE change_orders ADD COLUMN previous_amount DECIMAL(12, 2);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='change_orders' AND column_name='new_amount') THEN
        ALTER TABLE change_orders ADD COLUMN new_amount DECIMAL(12, 2);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='change_orders' AND column_name='status') THEN
        ALTER TABLE change_orders ADD COLUMN status TEXT DEFAULT 'pending';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='change_orders' AND column_name='approved_by') THEN
        ALTER TABLE change_orders ADD COLUMN approved_by TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='change_orders' AND column_name='approved_date') THEN
        ALTER TABLE change_orders ADD COLUMN approved_date DATE;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='change_orders' AND column_name='change_order_date') THEN
        ALTER TABLE change_orders ADD COLUMN change_order_date DATE DEFAULT CURRENT_DATE;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='change_orders' AND column_name='notes') THEN
        ALTER TABLE change_orders ADD COLUMN notes TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='change_orders' AND column_name='attachment_url') THEN
        ALTER TABLE change_orders ADD COLUMN attachment_url TEXT;
    END IF;
END $$;

-- ============================================
-- 5. CREATE INVOICES TABLE
-- ============================================
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
  amount_remaining DECIMAL(12, 2),
  
  -- Billing Period
  period_start DATE,
  period_end DATE,
  
  -- Progress Claims
  work_completed_percentage DECIMAL(5, 2),
  materials_supplied_percentage DECIMAL(5, 2),
  
  -- Status
  status TEXT DEFAULT 'pending',
  payment_date DATE,
  
  -- Matching to Contract
  matches_contract_scope BOOLEAN,
  variance_notes TEXT,
  
  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  -- File Storage
  invoice_file_url TEXT,
  ocr_text TEXT,
  
  -- Metadata
  notes TEXT,
  
  CONSTRAINT unique_invoice_number UNIQUE (subcontract_id, invoice_number)
);

-- ============================================
-- 6. CREATE INVOICE LINE ITEMS TABLE
-- ============================================
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
  variance_amount DECIMAL(12, 2),
  
  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- 7. CREATE PAYMENTS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS payments (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  invoice_id UUID REFERENCES invoices(id) ON DELETE CASCADE,
  subcontract_id UUID REFERENCES subcontracts(id) ON DELETE CASCADE,
  
  -- Payment Details
  payment_number TEXT NOT NULL,
  payment_date DATE NOT NULL,
  payment_amount DECIMAL(12, 2) NOT NULL,
  payment_method TEXT,
  check_number TEXT,
  
  -- Status
  status TEXT DEFAULT 'pending',
  
  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  -- Metadata
  notes TEXT,
  payment_file_url TEXT
);

-- ============================================
-- 8. CREATE HISTORICAL COST DATA TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS historical_cost_data (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  
  -- Work Classification
  work_category TEXT NOT NULL,
  work_type TEXT NOT NULL,
  unit TEXT NOT NULL,
  
  -- Cost Data
  unit_price DECIMAL(10, 2) NOT NULL,
  project_location TEXT,
  project_year INTEGER,
  
  -- Source
  source_subcontract_id UUID REFERENCES subcontracts(id) ON DELETE SET NULL,
  source_line_item_id UUID REFERENCES subcontract_line_items(id) ON DELETE SET NULL,
  
  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  -- Metadata
  notes TEXT
);

-- Create index for fast historical lookups
CREATE INDEX IF NOT EXISTS idx_historical_cost_lookup 
ON historical_cost_data(work_category, work_type, unit, project_location);

-- ============================================
-- 9. CREATE INDEXES FOR PERFORMANCE
-- ============================================
CREATE INDEX IF NOT EXISTS idx_subcontracts_project ON subcontracts(project_id);
CREATE INDEX IF NOT EXISTS idx_subcontracts_status ON subcontracts(status);
CREATE INDEX IF NOT EXISTS idx_invoices_subcontract ON invoices(subcontract_id);
CREATE INDEX IF NOT EXISTS idx_invoices_status ON invoices(status);
CREATE INDEX IF NOT EXISTS idx_change_orders_subcontract ON change_orders(subcontract_id);
CREATE INDEX IF NOT EXISTS idx_line_items_subcontract ON subcontract_line_items(subcontract_id);
CREATE INDEX IF NOT EXISTS idx_payments_invoice ON payments(invoice_id);

-- ============================================
-- 10. CREATE TRIGGERS FOR AUTO-UPDATES
-- ============================================

-- Function to update subcontract amount when change order is approved
CREATE OR REPLACE FUNCTION update_subcontract_amount()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.status = 'approved' AND (OLD.status IS NULL OR OLD.status != 'approved') THEN
    UPDATE subcontracts 
    SET current_amount = NEW.new_amount,
        updated_at = NOW()
    WHERE id = NEW.subcontract_id;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Drop trigger if exists, then create
DROP TRIGGER IF EXISTS change_order_approved ON change_orders;
CREATE TRIGGER change_order_approved
AFTER UPDATE ON change_orders
FOR EACH ROW
EXECUTE FUNCTION update_subcontract_amount();

-- Function to update invoice and subcontract amounts when payment is processed
CREATE OR REPLACE FUNCTION update_payment_amounts()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.status = 'processed' AND (OLD.status IS NULL OR OLD.status != 'processed') THEN
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

-- Drop trigger if exists, then create
DROP TRIGGER IF EXISTS payment_processed ON payments;
CREATE TRIGGER payment_processed
AFTER UPDATE ON payments
FOR EACH ROW
EXECUTE FUNCTION update_payment_amounts();

-- ============================================
-- MIGRATION COMPLETE
-- ============================================
-- All tables and columns are now set up!
-- You can now start using the database for contract tracking.

