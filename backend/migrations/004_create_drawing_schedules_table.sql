-- Migration: Create Drawing Schedules Table
-- Run this in your Supabase SQL Editor
-- Stores extracted schedule data from architectural drawings

-- ============================================
-- CREATE DRAWING SCHEDULES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS drawing_schedules (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  drawing_id UUID REFERENCES drawings(id) ON DELETE CASCADE,
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  
  -- Schedule Type
  schedule_type TEXT NOT NULL CHECK (schedule_type IN ('door', 'window', 'floor', 'ceiling', 'paint')),
  
  -- Item Details
  item_designation TEXT, -- e.g., "101", "W1", "Room 101"
  item_type TEXT, -- e.g., "Wood Door", "Fixed Window", "VCT Flooring"
  size TEXT, -- e.g., "3-0 x 7-0", "4-0 x 5-0", "SF"
  quantity INTEGER DEFAULT 1,
  
  -- Additional Details (JSON for flexibility)
  details JSONB, -- Hardware sets, glazing types, finish specs, manufacturer, etc.
  
  -- Location
  location TEXT, -- Room name or area
  
  -- Square Footage (for finishes)
  square_footage DECIMAL(10, 2),
  
  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_schedules_drawing_id ON drawing_schedules(drawing_id);
CREATE INDEX IF NOT EXISTS idx_schedules_project_id ON drawing_schedules(project_id);
CREATE INDEX IF NOT EXISTS idx_schedules_type ON drawing_schedules(schedule_type);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_schedule_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to auto-update updated_at
CREATE TRIGGER trigger_update_schedule_updated_at
  BEFORE UPDATE ON drawing_schedules
  FOR EACH ROW
  EXECUTE FUNCTION update_schedule_updated_at();

