-- Migration: Create Drawings Table
-- Run this in your Supabase SQL Editor
-- This creates a table to store architectural and engineering drawings

-- ============================================
-- CREATE DRAWINGS TABLE
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

-- Index for faster lookups
CREATE INDEX IF NOT EXISTS idx_drawings_project_id ON drawings(project_id);
CREATE INDEX IF NOT EXISTS idx_drawings_type ON drawings(drawing_type);
CREATE INDEX IF NOT EXISTS idx_drawings_current ON drawings(project_id, drawing_type, is_current) WHERE is_current = TRUE;

-- Function to update project drawing dates when new drawing is uploaded
CREATE OR REPLACE FUNCTION update_project_drawing_dates()
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

-- Trigger to automatically update project dates
CREATE TRIGGER trigger_update_project_drawing_dates
  AFTER INSERT OR UPDATE ON drawings
  FOR EACH ROW
  WHEN (NEW.is_current = TRUE)
  EXECUTE FUNCTION update_project_drawing_dates();

