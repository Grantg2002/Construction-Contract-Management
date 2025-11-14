-- Migration: Enhance scope_items table for flexible scope tracking
-- This adds all columns needed for your vision: pricing, breakdown levels, included/excluded

-- Add missing columns to scope_items table
ALTER TABLE scope_items
  -- Subcategory for breakdown levels (Level 2)
  ADD COLUMN IF NOT EXISTS subcategory TEXT,
  
  -- Component for extremely broken down items (Level 3) - optional
  ADD COLUMN IF NOT EXISTS component TEXT,
  
  -- Pricing fields
  ADD COLUMN IF NOT EXISTS quantity DECIMAL(10, 2),
  ADD COLUMN IF NOT EXISTS unit TEXT,  -- EA, SF, LF, HR, etc.
  ADD COLUMN IF NOT EXISTS unit_price DECIMAL(10, 2),
  ADD COLUMN IF NOT EXISTS line_total DECIMAL(12, 2),
  
  -- Included/Excluded flag
  ADD COLUMN IF NOT EXISTS is_included BOOLEAN DEFAULT TRUE,
  
  -- Breakdown level (1 = category only, 2 = category+subcategory, 3 = all levels)
  ADD COLUMN IF NOT EXISTS breakdown_level INTEGER DEFAULT 2,
  
  -- Display ordering
  ADD COLUMN IF NOT EXISTS display_order INTEGER DEFAULT 0,
  
  -- Timestamps
  ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_scope_items_subcontract ON scope_items(subcontract_id);
CREATE INDEX IF NOT EXISTS idx_scope_items_category ON scope_items(category);
CREATE INDEX IF NOT EXISTS idx_scope_items_included ON scope_items(is_included);

-- Create function to auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_scope_items_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for updated_at
DROP TRIGGER IF EXISTS scope_items_updated_at ON scope_items;
CREATE TRIGGER scope_items_updated_at
  BEFORE UPDATE ON scope_items
  FOR EACH ROW
  EXECUTE FUNCTION update_scope_items_updated_at();

-- Add comment to table explaining its purpose
COMMENT ON TABLE scope_items IS 'Stores flexible scope breakdown items for subcontracts. Supports unlimited scope items without schema changes.';

COMMENT ON COLUMN scope_items.category IS 'Level 1: Main category (e.g., "Electrical", "Plumbing")';
COMMENT ON COLUMN scope_items.subcategory IS 'Level 2: Subcategory (e.g., "Outlets", "Conduit")';
COMMENT ON COLUMN scope_items.component IS 'Level 3: Component (e.g., "GFCI Outlets") - for extremely broken down proposals';
COMMENT ON COLUMN scope_items.breakdown_level IS '1 = category only, 2 = category+subcategory, 3 = all levels';
COMMENT ON COLUMN scope_items.is_included IS 'TRUE = included in scope, FALSE = excluded (just notes)';
COMMENT ON COLUMN scope_items.unit IS 'Unit of measure: EA (each), SF (square feet), LF (linear feet), HR (hours), etc.';

