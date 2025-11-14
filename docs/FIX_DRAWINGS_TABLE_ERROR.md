# Fix for "column drawing_type does not exist" Error

## Problem
When running the drawings table migration, you got:
```
ERROR: 42703: column "drawing_type" does not exist
```

## Cause
This happens when:
1. The `drawings` table already exists (maybe from a previous attempt)
2. But it doesn't have the `drawing_type` column
3. The trigger tries to reference `drawing_type` before the column exists

## Solution

I've created a **FIXED migration** that handles all cases:

### File: `backend/migrations/003_create_drawings_table_FIXED.sql`

This migration:
1. ✅ Creates the table if it doesn't exist
2. ✅ Adds missing columns if table exists
3. ✅ Drops and recreates function/trigger to avoid conflicts
4. ✅ Handles all edge cases safely

## How to Fix

### Option 1: Use the Fixed Migration (Recommended)

1. **Open Supabase SQL Editor**
2. **Copy and paste** the entire contents of:
   ```
   backend/migrations/003_create_drawings_table_FIXED.sql
   ```
3. **Run it** - it will handle everything safely!

### Option 2: Manual Fix (If you want to check first)

1. **Check if table exists:**
   ```sql
   SELECT * FROM information_schema.tables 
   WHERE table_name = 'drawings';
   ```

2. **If table exists, check columns:**
   ```sql
   SELECT column_name, data_type 
   FROM information_schema.columns 
   WHERE table_name = 'drawings';
   ```

3. **Drop the table if it's incomplete:**
   ```sql
   DROP TABLE IF EXISTS drawings CASCADE;
   ```

4. **Then run the original migration:**
   ```sql
   -- Copy from 003_create_drawings_table.sql
   ```

## What the Fixed Migration Does

1. **Creates table** with all columns (if not exists)
2. **Adds missing columns** one by one (if table exists)
3. **Creates indexes** safely
4. **Drops old function/trigger** (if exists)
5. **Creates new function** with proper logic
6. **Creates trigger** that references the columns

## Verification

After running the fixed migration, verify it worked:

```sql
-- Check table exists
SELECT * FROM drawings LIMIT 1;

-- Check columns
SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'drawings'
ORDER BY ordinal_position;

-- Check trigger exists
SELECT trigger_name 
FROM information_schema.triggers 
WHERE event_object_table = 'drawings';
```

You should see:
- ✅ `drawing_type` column
- ✅ `drawing_date` column  
- ✅ `project_id` column
- ✅ `trigger_update_project_drawing_dates` trigger

## Next Steps

Once the migration runs successfully:
1. ✅ Test drawing upload via API
2. ✅ Verify trigger updates project dates
3. ✅ Continue with backend testing!

---

**The fixed migration is safe to run multiple times** - it won't break anything! 🚀

