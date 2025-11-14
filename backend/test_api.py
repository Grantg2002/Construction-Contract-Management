"""
Simple test script for testing the API endpoints
Run this after starting the backend server
"""
import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def test_upload_drawing(project_id: str, drawing_file_path: str, drawing_type: str, drawing_date: str):
    """Test drawing upload"""
    print(f"Testing drawing upload for project {project_id}...")
    
    with open(drawing_file_path, 'rb') as f:
        files = {'file': (Path(drawing_file_path).name, f, 'application/pdf')}
        data = {
            'drawing_type': drawing_type,
            'drawing_date': drawing_date,
            'architect_name': 'Test Architect' if drawing_type == 'architectural' else None,
            'engineer_name': 'Test Engineer' if drawing_type == 'engineering' else None,
        }
        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}
        
        response = requests.post(
            f"{BASE_URL}/api/projects/{project_id}/drawings",
            files=files,
            data=data
        )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
    return response.json()


def test_upload_proposal(project_id: str, proposal_file_path: str):
    """Test proposal upload and extraction"""
    print(f"Testing proposal upload for project {project_id}...")
    
    with open(proposal_file_path, 'rb') as f:
        files = {'file': (Path(proposal_file_path).name, f, 'application/pdf')}
        response = requests.post(
            f"{BASE_URL}/api/projects/{project_id}/proposals",
            files=files
        )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Subcontract ID: {result.get('subcontract_id')}")
        print(f"Company: {result.get('extracted_data', {}).get('company_name')}")
        print(f"Total Price: ${result.get('extracted_data', {}).get('total_price', 0):,.2f}")
        print(f"Extraction Cost: ${result.get('extraction_cost', 0):.4f}")
        print(f"\nScope Items Found: {len(result.get('extracted_data', {}).get('scope_items', []))}")
        print(f"Excluded Items: {len(result.get('extracted_data', {}).get('excluded_items', []))}")
        return result
    else:
        print(f"Error: {response.text}")
        return None


def test_generate_contract(subcontract_id: str):
    """Test contract generation"""
    print(f"Testing contract generation for subcontract {subcontract_id}...")
    
    subcontractor_data = {
        "company_name": "Test Subcontractor Inc.",
        "representative_name": "John Doe",
        "street": "123 Main St",
        "city": "Test City",
        "state": "CA",
        "zip": "12345",
        "email": "test@example.com",
        "phone": "555-1234",
        "fax": "555-5678"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/subcontracts/{subcontract_id}/generate-contract",
        json=subcontractor_data
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Contract HTML length: {len(result.get('contract_html', ''))} characters")
        
        # Save contract HTML to file for viewing
        output_file = Path("backend/test_contract_output.html")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result.get('contract_html', ''))
        print(f"Contract saved to: {output_file}")
        return result
    else:
        print(f"Error: {response.text}")
        return None


def test_get_drawings(project_id: str):
    """Test getting project drawings"""
    print(f"Testing get drawings for project {project_id}...")
    
    response = requests.get(f"{BASE_URL}/api/projects/{project_id}/drawings")
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
    return response.json()


if __name__ == "__main__":
    print("=" * 60)
    print("API Test Script")
    print("=" * 60)
    print()
    print("Make sure the backend server is running:")
    print("  cd backend")
    print("  python -m uvicorn main:app --reload")
    print()
    print("=" * 60)
    print()
    
    # Test health check
    test_health()
    
    # Example usage (uncomment and fill in your values):
    # PROJECT_ID = "your-project-uuid-here"
    # 
    # # Test drawing upload
    # test_upload_drawing(
    #     project_id=PROJECT_ID,
    #     drawing_file_path="path/to/drawing.pdf",
    #     drawing_type="architectural",
    #     drawing_date="2025-01-15"
    # )
    # 
    # # Test proposal upload
    # result = test_upload_proposal(
    #     project_id=PROJECT_ID,
    #     proposal_file_path="path/to/proposal.pdf"
    # )
    # 
    # if result:
    #     subcontract_id = result.get('subcontract_id')
    #     
    #     # Test contract generation
    #     test_generate_contract(subcontract_id)
    # 
    # # Test get drawings
    # test_get_drawings(PROJECT_ID)
    
    print("=" * 60)
    print("To test endpoints:")
    print("1. Fill in PROJECT_ID and file paths above")
    print("2. Uncomment the test calls")
    print("3. Run: python test_api.py")
    print()
    print("Or use FastAPI docs at: http://localhost:8000/docs")
    print("=" * 60)

