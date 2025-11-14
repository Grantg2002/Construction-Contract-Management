"""
Schedule Extractor - AI-powered extraction of schedules from architectural drawings
"""
import pdfplumber
from openai_handler import get_openai_client
from typing import Dict, List, Any
import json
import io


def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file"""
    try:
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            text_parts = []
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
            return "\n\n".join(text_parts)
    except Exception as e:
        raise Exception(f"Error extracting PDF text: {str(e)}")


async def extract_schedules_from_drawing(file_content: bytes, filename: str) -> Dict[str, List[Dict]]:
    """
    Extract door, window, and finish schedules from architectural drawing PDF
    
    Args:
        file_content: PDF file bytes
        filename: Name of the file
        
    Returns:
        Dictionary with extracted schedules:
        {
            "doors": [...],
            "windows": [...],
            "floors": [...],
            "ceilings": [...],
            "paint": [...]
        }
    """
    # Extract text from PDF
    raw_text = extract_text_from_pdf(file_content)
    
    # Use AI to extract schedules
    client = get_openai_client()
    
    system_prompt = """You are an expert at analyzing architectural drawing schedules. Extract structured data from door schedules, window schedules, and finish schedules.

EXTRACTION RULES:

1. DOOR SCHEDULES:
   - Look for tables or lists labeled "Door Schedule", "Door Schedule", or similar
   - Extract: designation (e.g., "101", "102A"), type (e.g., "Wood", "Metal", "Hollow Metal"), size (e.g., "3-0 x 7-0"), frame type, hardware set, quantity, location/room
   - If quantity not specified, assume 1

2. WINDOW SCHEDULES:
   - Look for tables or lists labeled "Window Schedule", "Window Schedule", or similar
   - Extract: designation (e.g., "W1", "W2"), type (e.g., "Fixed", "Casement", "Double-Hung"), size, glazing type, quantity, location

3. FINISH SCHEDULES:
   - Look for finish schedules (floors, ceilings, paint)
   - FLOORS: Extract room/area, finish type (e.g., "VCT", "Carpet", "Tile"), square footage
   - CEILINGS: Extract room/area, finish type (e.g., "Acoustic Tile", "Gypsum Board"), square footage
   - PAINT: Extract room/area, paint type/finish, square footage

Return valid JSON only."""

    user_prompt = f"""Extract all schedules from this architectural drawing:

{raw_text[:15000]}  # Limit to first 15K chars to avoid token limits

Return JSON in this exact format:
{{
  "doors": [
    {{
      "designation": "101",
      "type": "Wood Door",
      "size": "3-0 x 7-0",
      "frame": "Hollow Metal Frame",
      "hardware": "H1",
      "quantity": 1,
      "location": "Office 101"
    }}
  ],
  "windows": [
    {{
      "designation": "W1",
      "type": "Fixed Window",
      "size": "4-0 x 5-0",
      "glazing": "Double Pane",
      "quantity": 2,
      "location": "Office 101"
    }}
  ],
  "floors": [
    {{
      "room": "Office 101",
      "finish_type": "VCT",
      "square_footage": 120.5
    }}
  ],
  "ceilings": [
    {{
      "room": "Office 101",
      "finish_type": "Acoustic Tile",
      "square_footage": 120.5
    }}
  ],
  "paint": [
    {{
      "room": "Office 101",
      "paint_type": "Eggshell",
      "square_footage": 450.0
    }}
  ]
}}

If a schedule type is not found, return an empty array for that type."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
        cache_control={"type": "ephemeral"}  # Cache the system prompt
    )
    
    extracted_data = json.loads(response.choices[0].message.content)
    
    # Ensure all schedule types exist (even if empty)
    result = {
        "doors": extracted_data.get("doors", []),
        "windows": extracted_data.get("windows", []),
        "floors": extracted_data.get("floors", []),
        "ceilings": extracted_data.get("ceilings", []),
        "paint": extracted_data.get("paint", [])
    }
    
    return result


def format_schedule_for_database(schedule_data: Dict, drawing_id: str, project_id: str) -> List[Dict]:
    """
    Format extracted schedule data for database insertion
    
    Args:
        schedule_data: Dictionary from extract_schedules_from_drawing
        drawing_id: UUID of the drawing
        project_id: UUID of the project
        
    Returns:
        List of dictionaries ready for database insertion
    """
    items = []
    
    # Process doors
    for door in schedule_data.get("doors", []):
        items.append({
            "drawing_id": drawing_id,
            "project_id": project_id,
            "schedule_type": "door",
            "item_designation": door.get("designation"),
            "item_type": door.get("type"),
            "size": door.get("size"),
            "quantity": door.get("quantity", 1),
            "location": door.get("location"),
            "details": {
                "frame": door.get("frame"),
                "hardware": door.get("hardware")
            }
        })
    
    # Process windows
    for window in schedule_data.get("windows", []):
        items.append({
            "drawing_id": drawing_id,
            "project_id": project_id,
            "schedule_type": "window",
            "item_designation": window.get("designation"),
            "item_type": window.get("type"),
            "size": window.get("size"),
            "quantity": window.get("quantity", 1),
            "location": window.get("location"),
            "details": {
                "glazing": window.get("glazing")
            }
        })
    
    # Process floors
    for floor in schedule_data.get("floors", []):
        items.append({
            "drawing_id": drawing_id,
            "project_id": project_id,
            "schedule_type": "floor",
            "item_designation": floor.get("room"),
            "item_type": floor.get("finish_type"),
            "square_footage": floor.get("square_footage"),
            "location": floor.get("room"),
            "details": {}
        })
    
    # Process ceilings
    for ceiling in schedule_data.get("ceilings", []):
        items.append({
            "drawing_id": drawing_id,
            "project_id": project_id,
            "schedule_type": "ceiling",
            "item_designation": ceiling.get("room"),
            "item_type": ceiling.get("finish_type"),
            "square_footage": ceiling.get("square_footage"),
            "location": ceiling.get("room"),
            "details": {}
        })
    
    # Process paint
    for paint in schedule_data.get("paint", []):
        items.append({
            "drawing_id": drawing_id,
            "project_id": project_id,
            "schedule_type": "paint",
            "item_designation": paint.get("room"),
            "item_type": paint.get("paint_type"),
            "square_footage": paint.get("square_footage"),
            "location": paint.get("room"),
            "details": {}
        })
    
    return items

