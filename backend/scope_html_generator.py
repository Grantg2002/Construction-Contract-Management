"""
HTML Scope Generator
Generates clean HTML for scope of work (NO table, just CSS columns)
"""
from typing import List, Dict


def generate_scope_html(scope_items: List[Dict], excluded_items: List[str]) -> str:
    """
    Generate HTML scope of work with two columns (Included | Excluded)
    NO table - just CSS flexbox columns
    
    Args:
        scope_items: List of scope items with category, subcategory, description
        excluded_items: List of excluded item descriptions
        
    Returns:
        HTML string with clean formatting (no borders, no table)
    """
    # Group included items by category
    included_by_category = {}
    for item in scope_items:
        if item.get("is_included", True):
            category = item.get("category", "Other")
            subcategory = item.get("subcategory")
            description = item.get("description", "")
            
            if category not in included_by_category:
                included_by_category[category] = []
            
            # Format: "Subcategory: Description" or just "Description"
            if subcategory:
                formatted_desc = f"<strong>{subcategory}:</strong> {description}"
            else:
                formatted_desc = description
            
            included_by_category[category].append(formatted_desc)
    
    # Build included items HTML
    included_html_parts = []
    for category, items in included_by_category.items():
        category_html = f'<p><strong>{category}</strong></p>'
        items_html = '<br>'.join(f'<p>{item}</p>' for item in items)
        included_html_parts.append(f'{category_html}{items_html}')
    
    included_html = '\n    '.join(included_html_parts) if included_html_parts else '<p>No included items specified.</p>'
    
    # Build excluded items HTML
    excluded_html = ''
    if excluded_items:
        excluded_html = '\n    '.join(f'<p>• {item}</p>' for item in excluded_items)
    else:
        excluded_html = '<p>No excluded items specified.</p>'
    
    # Combine into two-column layout (NO table, just CSS flexbox)
    html = f'''<div style="display: flex; gap: 30px; margin: 20px 0;">
  <div style="flex: 1;">
    <h3 style="margin-top: 0; margin-bottom: 15px;">INCLUDED ITEMS</h3>
    {included_html}
  </div>
  
  <div style="flex: 1;">
    <h3 style="margin-top: 0; margin-bottom: 15px;">EXCLUDED ITEMS</h3>
    {excluded_html}
  </div>
</div>'''
    
    return html

