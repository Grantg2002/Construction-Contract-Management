"""
Comprehensive schema inspection - Get all table structures
"""
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def inspect_full_schema():
    """Get detailed schema for all tables"""
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    
    if not supabase_url or not supabase_key:
        print("[ERROR] Missing credentials in .env file")
        return
    
    print("=" * 80)
    print("COMPREHENSIVE SUPABASE SCHEMA INSPECTION")
    print("=" * 80)
    print(f"URL: {supabase_url}\n")
    
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json"
    }
    
    # All tables from your dashboard
    tables = [
        'projects',
        'subcontracts',
        'change_orders',
        'drawings',
        'draws',
        'historical_cost_data',
        'invoice_line_items',
        'invoices',
        'payments',
        'scope_items',
        'subcontract_line_items',
        'api_usage_log'
    ]
    
    schema_info = {}
    
    for table_name in tables:
        print(f"\n{'='*80}")
        print(f"TABLE: {table_name}")
        print('='*80)
        
        try:
            # Try to get table structure by querying with limit 0 or getting one row
            url = f"{supabase_url}/rest/v1/{table_name}?select=*&limit=1"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data and len(data) > 0:
                    print("COLUMNS:")
                    print("-" * 80)
                    columns = {}
                    for key, value in data[0].items():
                        value_type = type(value).__name__
                        columns[key] = {
                            'type': value_type,
                            'example': value if value is not None and len(str(value)) < 100 else None
                        }
                        example_str = f" (Example: {value})" if value is not None and len(str(value)) < 100 else ""
                        print(f"  - {key:30} Type: {value_type:15}{example_str}")
                    
                    schema_info[table_name] = columns
                    print(f"\n[STATUS] Table exists with {len(columns)} columns")
                    
                else:
                    print("[STATUS] Table exists but is empty")
                    # Try to infer structure from Supabase metadata
                    # We'll need to check manually or use a different approach
                    schema_info[table_name] = "exists_but_empty"
                    
            elif response.status_code == 404:
                print("[STATUS] Table NOT FOUND")
                schema_info[table_name] = "not_found"
            else:
                print(f"[ERROR] Status code: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                schema_info[table_name] = f"error_{response.status_code}"
                
        except Exception as e:
            print(f"[ERROR] {str(e)}")
            schema_info[table_name] = f"error: {str(e)}"
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    existing = [t for t, s in schema_info.items() if isinstance(s, dict) or s == "exists_but_empty"]
    not_found = [t for t, s in schema_info.items() if s == "not_found"]
    errors = [t for t, s in schema_info.items() if isinstance(s, str) and s.startswith("error")]
    
    print(f"\n[OK] Existing tables: {len(existing)}")
    for t in existing:
        print(f"   - {t}")
    
    if not_found:
        print(f"\n[NOT FOUND] Missing tables: {len(not_found)}")
        for t in not_found:
            print(f"   - {t}")
    
    if errors:
        print(f"\n[ERRORS] Tables with errors: {len(errors)}")
        for t in errors:
            print(f"   - {t}: {schema_info[t]}")
    
    # Save to file for reference
    output_file = "docs/current_schema_structure.json"
    with open(output_file, 'w') as f:
        json.dump(schema_info, f, indent=2, default=str)
    
    print(f"\n[SAVED] Schema info saved to: {output_file}")
    print("=" * 80)
    
    return schema_info

if __name__ == "__main__":
    inspect_full_schema()

