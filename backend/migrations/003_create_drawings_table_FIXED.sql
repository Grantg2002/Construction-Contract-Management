-- Migration: Create Drawings Table (FIXED VERSION)
-- Run this in your Supabase SQL Editor
-- This creates a table to store architectural and engineering drawings
-- Handles case where table might already exist

-- ============================================
-- STEP 1: CREATE DRAWINGS TABLE (if not exists)
-- ============================================
CREATE TABLE IF NOT EXISTS drawings (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  
  -- Drawing Type
  drawing_type TEXT NOT NULL CHECK (drawing_type IN ('architectural', 'engineering')),
  
  -- Drawing Information
  drawing_date DATE NOT NULL,
  revision_number TEXT,
  drawing_title TEXT,
  
  -- Team Information
  architect_name TEXT, -- For architectural drawings
  engineer_name TEXT,  -- For engineering drawings
  
  -- File Storage
  file_url TEXT,
  file_name TEXT,
  file_size INTEGER, -- in bytes
  
  -- Metadata
  notes TEXT,
  is_current BOOLEAN DEFAULT TRUE, -- Latest revision
  
  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- STEP 2: ADD MISSING COLUMNS (if table exists but columns missing)
-- ============================================
DO $$ 
BEGIN
    -- Drawing Type
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='drawings' AND column_name='drawing_type') THEN
        ALTER TABLE drawings ADD COLUMN drawing_type TEXT;
        -- Add constraint after column exists
        ALTER TABLE drawings ADD CONSTRAINT drawings_drawing_type_check 
            CHECK (drawing_type IN ('architectural', 'engineering'));
        -- Make it NOT NULL if table is empty
        ALTER TABLE drawings ALTER COLUMN drawing_type SET NOT NULL;
    END IF;
    
    -- Drawing Information
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='drawings' AND column_name='drawing_date') THEN
        ALTER TABLE drawings ADD COLUMN drawing_date DATE NOT NULL DEFAULT CURRENT_DATE;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='drawings' AND column_name='revision_number') THEN
        ALTER TABLE drawings ADD COLUMN revision_number TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='drawings' AND column_name='drawing_title') THEN
        ALTER TABLE drawings ADD COLUMN drawing_title TEXT;
    END IF;
    
    -- Team Information
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='drawings' AND column_name='architect_name') THEN
        ALTER TABLE drawings ADD COLUMN architect_name TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='drawings' AND column_name='engineer_name') THEN
        ALTER TABLE drawings ADD COLUMN engineer_name TEXT;
    END IF;
    
    -- File Storage
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='drawings' AND column_name='file_url') THEN
        ALTER TABLE drawings ADD COLUMN file_url TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='drawings' AND column_name='file_name') THEN
        ALTER TABLE drawings ADD COLUMN file_name TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='drawings' AND column_name='file_size') THEN
        ALTER TABLE drawings ADD COLUMN file_size INTEGER;
    END IF;
    
    -- Metadata
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='drawings' AND column_name='notes') THEN
        ALTER TABLE drawings ADD COLUMN notes TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='drawings' AND column_name='is_current') THEN
        ALTER TABLE drawings ADD COLUMN is_current BOOLEAN DEFAULT TRUE;
    END IF;
    
    -- Timestamps
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='drawings' AND column_name='created_at') THEN
        ALTER TABLE drawings ADD COLUMN created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='drawings' AND column_name='updated_at') THEN
        ALTER TABLE drawings ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
    END IF;
    
    -- Project ID foreign key (if missing)
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints 
        WHERE table_name='drawings' 
        AND constraint_name='drawings_project_id_fkey'
    ) THEN
        -- Check if project_id column exists first
        IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='drawings' AND column_name='project_id') THEN
            ALTER TABLE drawings ADD CONSTRAINT drawings_project_id_fkey 
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE;
        ELSE
            ALTER TABLE drawings ADD COLUMN project_id UUID REFERENCES projects(id) ON DELETE CASCADE;
        END IF;
    END IF;
END $$;

-- ============================================
-- STEP 3: CREATE INDEXES
-- ============================================
CREATE INDEX IF NOT EXISTS idx_drawings_project_id ON drawings(project_id);
CREATE INDEX IF NOT EXISTS idx_drawings_type ON drawings(drawing_type);
CREATE INDEX IF NOT EXISTS idx_drawings_current ON drawings(project_id, drawing_type, is_current) WHERE is_current = TRUE;

-- ============================================
-- STEP 4: CREATE FUNCTION (drop and recreate to avoid conflicts)
-- ============================================
DROP FUNCTION IF EXISTS update_project_drawing_dates() CASCADE;

CREATE FUNCTION update_project_drawing_dates()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.drawing_type = 'architectural' AND NEW.is_current = TRUE THEN
    UPDATE projects 
    SET drawings_date = NEW.drawing_date,
        architect = COALESCE(NEW.architect_name, projects.architect)
    WHERE id = NEW.project_id;
  END IF;
  
  IF NEW.drawing_type = 'engineering' AND NEW.is_current = TRUE THEN
    UPDATE projects 
    SET engineering_date = NEW.drawing_date,
        engineer = COALESCE(NEW.engineer_name, projects.engineer)
    WHERE id = NEW.project_id;
  END IF;
  
  -- Mark other drawings of same type as not current
  UPDATE drawings
  SET is_current = FALSE
  WHERE project_id = NEW.project_id
    AND drawing_type = NEW.drawing_type
    AND id != NEW.id
    AND is_current = TRUE;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- STEP 5: CREATE TRIGGER (drop first if exists)
-- ============================================
DROP TRIGGER IF EXISTS trigger_update_project_drawing_dates ON drawings;

CREATE TRIGGER trigger_update_project_drawing_dates
  AFTER INSERT OR UPDATE ON drawings
  FOR EACH ROW
  WHEN (NEW.is_current = TRUE)
  EXECUTE FUNCTION update_project_drawing_dates();

