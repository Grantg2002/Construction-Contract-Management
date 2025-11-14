"""
Proposal Analyzer - Analyze uploaded proposals to understand breakdown patterns
This will help us understand how different proposals structure their scope
"""
import os
import sys
from pathlib import Path
from typing import Dict, List, Any
import json

# Try to import PDF libraries (install if needed)
try:
    import pdfplumber
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("[WARNING] pdfplumber not installed. Install with: pip install pdfplumber")

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False
    print("[WARNING] python-docx not installed. Install with: pip install python-docx")


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF file"""
    if not PDF_AVAILABLE:
        raise ImportError("pdfplumber not installed. Run: pip install pdfplumber")
    
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
            text += "\n"
    return text


def extract_text_from_docx(docx_path: str) -> str:
    """Extract text from Word document"""
    if not DOCX_AVAILABLE:
        raise ImportError("python-docx not installed. Run: pip install python-docx")
    
    doc = Document(docx_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    
    # Also extract from tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                text += cell.text + " | "
            text += "\n"
    
    return text


def analyze_proposal_structure(text: str, filename: str) -> Dict[str, Any]:
    """
    Analyze proposal to understand its breakdown structure
    
    Returns analysis of:
    - Breakdown level (1, 2, or 3)
    - Categories found
    - Subcategories found
    - Components found
    - Pricing structure
    """
    analysis = {
        "filename": filename,
        "breakdown_level": None,
        "categories": [],
        "subcategories": [],
        "components": [],
        "has_pricing": False,
        "has_quantities": False,
        "has_units": False,
        "structure_pattern": None,
        "sample_lines": []
    }
    
    lines = text.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    
    # Look for patterns indicating breakdown levels
    # Level 3 indicators: Very detailed breakdown (e.g., "Electrical > Outlets > GFCI")
    # Level 2 indicators: Category > Subcategory
    # Level 1 indicators: Just category names
    
    category_patterns = []
    subcategory_patterns = []
    component_patterns = []
    
    # Common construction categories
    common_categories = [
        "electrical", "plumbing", "hvac", "framing", "drywall", "paint", 
        "flooring", "roofing", "concrete", "earthwork", "excavation",
        "insulation", "siding", "windows", "doors", "suspended ceiling",
        "metal framing", "wood framing"
    ]
    
    # Look for pricing indicators
    has_dollar_signs = any('$' in line for line in non_empty_lines)
    has_numbers = any(any(char.isdigit() for char in line) for line in non_empty_lines)
    
    # Look for unit indicators
    units = ['EA', 'SF', 'LF', 'SY', 'CY', 'HR', 'LS', 'TON', 'GAL']
    has_units = any(unit in text.upper() for unit in units)
    
    # Sample some lines for manual review
    sample_lines = non_empty_lines[:20]  # First 20 non-empty lines
    
    analysis.update({
        "has_pricing": has_dollar_signs,
        "has_quantities": has_numbers,
        "has_units": has_units,
        "sample_lines": sample_lines,
        "total_lines": len(non_empty_lines),
        "total_length": len(text)
    })
    
    # Try to detect structure
    # Look for hierarchical patterns
    if '>' in text or '→' in text or ':' in text:
        # Might have hierarchical structure
        analysis["structure_pattern"] = "hierarchical"
    
    # Look for table-like structure
    if '|' in text or '\t' in text:
        analysis["structure_pattern"] = "table"
    
    # Look for bullet points
    if any(line.startswith(('•', '-', '*')) for line in non_empty_lines):
        analysis["structure_pattern"] = "bulleted"
    
    return analysis


def analyze_proposal_file(file_path: str) -> Dict[str, Any]:
    """Analyze a single proposal file"""
    path = Path(file_path)
    
    if not path.exists():
        return {"error": f"File not found: {file_path}"}
    
    filename = path.name
    file_ext = path.suffix.lower()
    
    print(f"\n{'='*80}")
    print(f"ANALYZING: {filename}")
    print('='*80)
    
    try:
        if file_ext == '.pdf':
            if not PDF_AVAILABLE:
                return {"error": "PDF support not available. Install pdfplumber"}
            text = extract_text_from_pdf(str(path))
        elif file_ext in ['.doc', '.docx']:
            if not DOCX_AVAILABLE:
                return {"error": "Word document support not available. Install python-docx"}
            text = extract_text_from_docx(str(path))
        elif file_ext in ['.txt', '.md']:
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            return {"error": f"Unsupported file type: {file_ext}"}
        
        analysis = analyze_proposal_structure(text, filename)
        analysis["extracted_text_preview"] = text[:1000]  # First 1000 chars
        
        return analysis
        
    except Exception as e:
        return {"error": f"Error analyzing file: {str(e)}"}


def main():
    """Main function to analyze proposals"""
    if len(sys.argv) < 2:
        print("Usage: python proposal_analyzer.py <proposal_file1> [proposal_file2] ...")
        print("\nExample:")
        print("  python proposal_analyzer.py proposals/earthworks.pdf proposals/paint_team.pdf")
        return
    
    files = sys.argv[1:]
    results = []
    
    for file_path in files:
        result = analyze_proposal_file(file_path)
        results.append(result)
        
        if "error" in result:
            print(f"\n[ERROR] {result['error']}")
        else:
            print(f"\n[ANALYSIS RESULTS]")
            print(f"  Breakdown Level: {result.get('breakdown_level', 'Unknown')}")
            print(f"  Has Pricing: {result.get('has_pricing', False)}")
            print(f"  Has Quantities: {result.get('has_quantities', False)}")
            print(f"  Has Units: {result.get('has_units', False)}")
            print(f"  Structure Pattern: {result.get('structure_pattern', 'Unknown')}")
            print(f"  Total Lines: {result.get('total_lines', 0)}")
            print(f"\n  Sample Lines:")
            for i, line in enumerate(result.get('sample_lines', [])[:10], 1):
                print(f"    {i}. {line[:80]}...")
    
    # Save results to JSON
    output_file = "docs/proposal_analysis_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n{'='*80}")
    print(f"[SAVED] Analysis results saved to: {output_file}")
    print('='*80)


if __name__ == "__main__":
    main()

