"""
Check scope_items table structure in Supabase
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def check_scope_items_schema():
    """Get the structure of scope_items table"""
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    
    if not supabase_url or not supabase_key:
        print("[ERROR] Missing credentials")
        return
    
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    
    print("=" * 80)
    print("CHECKING scope_items TABLE STRUCTURE")
    print("=" * 80)
    print(f"URL: {supabase_url}\n")
    
    # Method 1: Try to query table structure via REST API
    # Supabase REST API might return column info in headers or error messages
    
    url = f"{supabase_url}/rest/v1/scope_items"
    
    # Try a SELECT query to see what columns exist
    # Use limit 0 to avoid data, just get structure
    try:
        response = requests.get(
            f"{url}?select=*&limit=0",
            headers=headers,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # Check response headers for column info
            print("\nResponse Headers:")
            for key, value in response.headers.items():
                if 'content' in key.lower() or 'range' in key.lower():
                    print(f"  {key}: {value}")
            
            # Try to get column names by attempting a query
            # Even with limit 0, we might get column info
            data = response.json()
            print(f"\nResponse Data: {data}")
            
        elif response.status_code == 406:
            # This might indicate we need to specify columns
            print("\n[INFO] Need to specify columns - trying different approach...")
            
    except Exception as e:
        print(f"[ERROR] {str(e)}")
    
    # Method 2: Try to insert a test row (will fail but show us structure)
    print("\n" + "=" * 80)
    print("METHOD 2: Attempting test insert to see expected structure")
    print("=" * 80)
    
    test_data = {
        "description": "test",
        "quantity": 1,
        "unit": "EA",
        "unit_price": 100.00
    }
    
    try:
        response = requests.post(
            url,
            headers=headers,
            json=test_data,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
        if response.status_code == 201:
            # Success! Delete the test row
            test_id = response.json()[0].get('id')
            if test_id:
                delete_url = f"{url}?id=eq.{test_id}"
                requests.delete(delete_url, headers=headers)
                print(f"\n[OK] Test row created and deleted. Columns exist!")
                
                # Get the structure from the response
                columns = list(response.json()[0].keys())
                print(f"\n[FOUND] Columns in scope_items table:")
                print("-" * 80)
                for col in columns:
                    print(f"  - {col}")
                return columns
                
    except Exception as e:
        print(f"[ERROR] {str(e)}")
    
    # Method 3: Try querying with specific common column names
    print("\n" + "=" * 80)
    print("METHOD 3: Testing common column names")
    print("=" * 80)
    
    common_columns = [
        'id', 'subcontract_id', 'category', 'subcategory', 'description',
        'quantity', 'unit', 'unit_price', 'line_total', 'is_included',
        'display_order', 'created_at', 'updated_at'
    ]
    
    found_columns = []
    
    for col in common_columns:
        try:
            test_url = f"{url}?select={col}&limit=1"
            response = requests.get(test_url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                found_columns.append(col)
                print(f"  [OK] {col} exists")
            elif response.status_code == 400:
                # Column doesn't exist or wrong name
                print(f"  [NOT FOUND] {col}")
            else:
                print(f"  [UNKNOWN] {col} - Status: {response.status_code}")
                
        except Exception as e:
            print(f"  [ERROR] {col}: {str(e)}")
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    if found_columns:
        print(f"\n[FOUND] {len(found_columns)} columns:")
        for col in found_columns:
            print(f"  - {col}")
    else:
        print("\n[WARNING] Could not determine column structure automatically")
        print("You may need to check Supabase dashboard manually")
    
    print("\n" + "=" * 80)
    
    return found_columns

if __name__ == "__main__":
    check_scope_items_schema()

