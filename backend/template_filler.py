"""
Template Filler Service
Fills placeholders in HTML template with extracted data
"""
from typing import Dict, Optional
from datetime import datetime
from supabase_client import get_supabase_client


async def get_project_data(project_id: str) -> Dict:
    """Get project data including latest drawing dates"""
    supabase = get_supabase_client()
    
    # Get project
    project_result = supabase.table("projects").select("*").eq("id", project_id).single().execute()
    project = project_result.data
    
    # Get latest drawings (handle case where they don't exist)
    try:
        arch_drawing = supabase.table("drawings")\
            .select("*")\
            .eq("project_id", project_id)\
            .eq("drawing_type", "architectural")\
            .eq("is_current", True)\
            .single()\
            .execute()
        arch_data = arch_drawing.data if arch_drawing.data else {}
    except:
        arch_data = {}
    
    try:
        eng_drawing = supabase.table("drawings")\
            .select("*")\
            .eq("project_id", project_id)\
            .eq("drawing_type", "engineering")\
            .eq("is_current", True)\
            .single()\
            .execute()
        eng_data = eng_drawing.data if eng_drawing.data else {}
    except:
        eng_data = {}
    
    return {
        "project": project,
        "architectural_drawing": arch_data,
        "engineering_drawing": eng_data
    }


def fill_template(template_html: str, placeholders: Dict[str, str]) -> str:
    """
    Fill placeholders in HTML template
    
    Args:
        template_html: HTML template with {{placeholder}} syntax
        placeholders: Dictionary mapping placeholder names to values
        
    Returns:
        Filled HTML string
    """
    filled_html = template_html
    
    # Replace all placeholders
    for placeholder, value in placeholders.items():
        # Handle both {{placeholder}} and {{placeholder}} with HTML entities
        placeholder_pattern = "{{" + placeholder + "}}"
        filled_html = filled_html.replace(placeholder_pattern, str(value))
        # Also handle HTML entity version
        html_entity_pattern = "{{<span class=SpellE><span class=GramE>" + placeholder + "</span></span>}}"
        filled_html = filled_html.replace(html_entity_pattern, str(value))
    
    return filled_html


async def generate_contract_html(
    project_id: str,
    subcontractor_data: Dict,
    scope_html: str,
    proposal_date: str,
    total_price: float
) -> str:
    """
    Generate filled contract HTML from template
    
    Args:
        project_id: Project UUID
        subcontractor_data: Dict with company_name, street, city, state, zip, email, phone, fax, representative_name
        scope_html: Generated HTML scope of work
        proposal_date: Proposal date (YYYY-MM-DD)
        total_price: Total contract amount
        
    Returns:
        Filled HTML contract
    """
    # Get project and drawing data
    project_data = await get_project_data(project_id)
    project = project_data["project"]
    arch_drawing = project_data["architectural_drawing"]
    eng_drawing = project_data["engineering_drawing"]
    
    # Read template (try both relative paths)
    import os
    template_paths = [
        "templates/subcontract_template.htm",
        "backend/templates/subcontract_template.htm",
        os.path.join(os.path.dirname(__file__), "templates", "subcontract_template.htm")
    ]
    template_html = None
    for path in template_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                template_html = f.read()
            break
    
    if not template_html:
        raise FileNotFoundError(f"Template not found. Tried: {template_paths}")
    
    # Format dates
    drawings_date = arch_drawing.get("drawing_date", project.get("drawings_date", ""))
    engineering_date = eng_drawing.get("drawing_date", project.get("engineering_date", ""))
    
    if drawings_date:
        if isinstance(drawings_date, str):
            drawings_date_str = drawings_date
        else:
            drawings_date_str = drawings_date.strftime("%B %d, %Y") if hasattr(drawings_date, 'strftime') else str(drawings_date)
    else:
        drawings_date_str = ""
    
    if engineering_date:
        if isinstance(engineering_date, str):
            engineering_date_str = engineering_date
        else:
            engineering_date_str = engineering_date.strftime("%B %d, %Y") if hasattr(engineering_date, 'strftime') else str(engineering_date)
    else:
        engineering_date_str = ""
    
    # Format proposal date
    try:
        proposal_date_obj = datetime.strptime(proposal_date, "%Y-%m-%d")
        proposal_date_formatted = proposal_date_obj.strftime("%B %d, %Y")
    except:
        proposal_date_formatted = proposal_date
    
    # Format price
    price_formatted = f"${total_price:,.2f}"
    
    # Build placeholders dictionary
    placeholders = {
        # Project info
        "project.name": project.get("name", ""),
        "project.street": project.get("street", ""),
        "project.city": project.get("city", ""),
        "project.state": project.get("state", ""),
        "project.zip": project.get("zip", ""),
        
        # Team info
        "architect": arch_drawing.get("architect_name", project.get("architect", "")),
        "engineer": eng_drawing.get("engineer_name", project.get("engineer", "")),
        "pm.name": project.get("pm_name", ""),
        "pm.number": project.get("pm_phone", ""),
        
        # Drawing dates
        "drawings.date": drawings_date_str,
        "engineering.date": engineering_date_str,
        
        # Subcontractor info
        "sub.company": subcontractor_data.get("company_name", ""),
        "sub.rep": subcontractor_data.get("representative_name", ""),
        "sub.street": subcontractor_data.get("street", ""),
        "sub.city": subcontractor_data.get("city", ""),
        "sub.state": subcontractor_data.get("state", ""),
        "sub.zip": subcontractor_data.get("zip", ""),
        "sub.email": subcontractor_data.get("email", ""),
        "sub.phone": subcontractor_data.get("phone", ""),
        "sub.fax": subcontractor_data.get("fax", ""),
        
        # Proposal info
        "proposal.date": proposal_date_formatted,
        "proposal.pricing": price_formatted,
        
        # Scope
        "scope.html": scope_html
    }
    
    # Fill template
    filled_html = fill_template(template_html, placeholders)
    
    return filled_html

