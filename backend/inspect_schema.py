"""
Script to inspect Supabase database schema
Run this to see your current table structure
"""
import os
from supabase_client import get_supabase_client
from dotenv import load_dotenv

load_dotenv()

def inspect_schema():
    """Query and display the database schema"""
    try:
        supabase = get_supabase_client()
        
        # Query information_schema to get table structure
        # Note: This requires direct SQL access, so we'll use a different approach
        # Let's try to query each table to see its structure
        
        print("=" * 60)
        print("SUPABASE DATABASE SCHEMA INSPECTION")
        print("=" * 60)
        print()
        
        # Try to get a sample row from each table to infer structure
        tables_to_check = ['projects', 'subcontracts']
        
        for table_name in tables_to_check:
            print(f"\n📊 Table: {table_name}")
            print("-" * 60)
            try:
                # Get first row to see structure
                result = supabase.table(table_name).select("*").limit(1).execute()
                
                if result.data and len(result.data) > 0:
                    print("Columns found:")
                    for key in result.data[0].keys():
                        value = result.data[0][key]
                        value_type = type(value).__name__
                        print(f"  - {key}: {value_type}")
                        if value is not None:
                            print(f"    Example: {value}")
                else:
                    print(f"  Table exists but is empty")
                    # Try to get table info another way
                    print(f"  (Table structure will be inferred from your Supabase dashboard)")
                    
            except Exception as e:
                print(f"  ⚠️  Error querying table: {str(e)}")
                print(f"  Table might not exist or have different name")
        
        print("\n" + "=" * 60)
        print("To see full schema, check your Supabase Dashboard:")
        print("  Table Editor → Select table → View columns")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error connecting to Supabase: {str(e)}")
        print("\nMake sure your .env file has:")
        print("  SUPABASE_URL=your_url")
        print("  SUPABASE_ANON_KEY=your_key")

if __name__ == "__main__":
    inspect_schema()

