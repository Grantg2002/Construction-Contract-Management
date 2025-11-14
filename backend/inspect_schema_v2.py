"""
Enhanced schema inspection using Supabase REST API
Works without needing Python supabase package installed
"""
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def inspect_schema():
    """Query Supabase to inspect database schema"""
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    
    if not supabase_url or not supabase_key:
        print("[ERROR] Missing SUPABASE_URL or SUPABASE_ANON_KEY in .env file")
        print("   Run: python setup_env.py")
        return
    
    print("=" * 70)
    print("SUPABASE DATABASE SCHEMA INSPECTION")
    print("=" * 70)
    print(f"URL: {supabase_url}")
    print()
    
    # Tables to check
    tables_to_check = [
        'projects',
        'subcontracts',
        'subcontract_line_items',
        'change_orders',
        'invoices',
        'invoice_line_items',
        'payments',
        'historical_cost_data'
    ]
    
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json"
    }
    
    found_tables = []
    missing_tables = []
    
    for table_name in tables_to_check:
        try:
            # Try to query the table (limit 0 to just check if it exists)
            url = f"{supabase_url}/rest/v1/{table_name}?select=*&limit=1"
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                found_tables.append(table_name)
                data = response.json()
                
                print(f"[OK] Table: {table_name}")
                print("-" * 70)
                
                if data and len(data) > 0:
                    # Show column structure from first row
                    print("Columns found:")
                    for key in data[0].keys():
                        value = data[0][key]
                        value_type = type(value).__name__
                        print(f"  - {key:30} ({value_type})")
                        if value is not None and len(str(value)) < 50:
                            print(f"    Example: {value}")
                else:
                    print("  (Table exists but is empty)")
                
                print()
                
            elif response.status_code == 404:
                missing_tables.append(table_name)
                print(f"[NOT FOUND] Table: {table_name}")
                print()
            else:
                print(f"[ERROR] Table: {table_name} - Error {response.status_code}")
                print(f"   Response: {response.text[:100]}")
                print()
                
        except Exception as e:
            print(f"[ERROR] Error checking {table_name}: {str(e)}")
            print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"[OK] Found tables: {len(found_tables)}")
    if found_tables:
        for t in found_tables:
            print(f"   - {t}")
    
    print(f"\n[NOT FOUND] Missing tables: {len(missing_tables)}")
    if missing_tables:
        for t in missing_tables:
            print(f"   - {t}")
    
    print("\n" + "=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    if missing_tables:
        print("1. Review the schema design: docs/DATABASE_SCHEMA_DESIGN.md")
        print("2. Run migration script to create missing tables")
        print("3. Add missing columns to existing tables")
    else:
        print("[OK] All tables exist! Ready to proceed.")
    print("=" * 70)

if __name__ == "__main__":
    inspect_schema()

