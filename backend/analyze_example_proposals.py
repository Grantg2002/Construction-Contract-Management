"""
Analyze the example proposals from the Example Proposals folder
"""
import os
import sys
import json
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("[ERROR] pdfplumber not installed. Installing...")
    os.system("pip install pdfplumber")
    import pdfplumber

PROPOSALS_PATH = r"C:\Users\Grant\OneDrive - Fusion Properties\Desktop\Half-baked Code\Construction Contract Management\Example Proposals (PDFs)"

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF"""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"  [ERROR] Could not extract text: {e}")
    return text

def analyze_proposal(pdf_path: Path):
    """Analyze a single proposal"""
    filename = pdf_path.name
    print(f"\n{'='*80}")
    print(f"ANALYZING: {filename}")
    print('='*80)
    
    # Extract text
    print("Extracting text...")
    text = extract_text_from_pdf(str(pdf_path))
    
    if not text or len(text.strip()) < 50:
        print(f"  [WARNING] Very little text extracted ({len(text)} chars)")
        return None
    
    # Analyze structure
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    analysis = {
        "filename": filename,
        "total_chars": len(text),
        "total_lines": len(lines),
        "has_dollar_signs": '$' in text,
        "has_numbers": any(char.isdigit() for char in text),
        "sample_lines": lines[:30],  # First 30 lines
        "full_text_preview": text[:2000]  # First 2000 chars
    }
    
    # Look for structure patterns
    has_hierarchy = any('>' in line or '→' in line or ':' in line for line in lines[:50])
    has_table = any('|' in line or '\t' in line for line in lines[:50])
    has_bullets = any(line.startswith(('•', '-', '*', '·')) for line in lines[:50])
    
    analysis["structure_pattern"] = []
    if has_hierarchy:
        analysis["structure_pattern"].append("hierarchical")
    if has_table:
        analysis["structure_pattern"].append("table")
    if has_bullets:
        analysis["structure_pattern"].append("bulleted")
    if not analysis["structure_pattern"]:
        analysis["structure_pattern"].append("paragraph")
    
    # Look for common construction terms
    text_lower = text.lower()
    categories_found = []
    common_cats = ["electrical", "plumbing", "hvac", "framing", "drywall", "paint", 
                   "flooring", "roofing", "concrete", "earthwork", "excavation",
                   "insulation", "siding", "windows", "doors", "ceiling", "metal"]
    
    for cat in common_cats:
        if cat in text_lower:
            categories_found.append(cat)
    
    analysis["categories_detected"] = categories_found
    
    # Look for pricing patterns
    import re
    dollar_amounts = re.findall(r'\$[\d,]+\.?\d*', text)
    analysis["dollar_amounts_found"] = len(dollar_amounts)
    analysis["sample_dollar_amounts"] = dollar_amounts[:10]
    
    # Look for unit patterns
    units = ['EA', 'SF', 'LF', 'SY', 'CY', 'HR', 'LS', 'TON', 'GAL', 'SQ FT', 'LIN FT']
    units_found = []
    for unit in units:
        if unit in text.upper():
            units_found.append(unit)
    analysis["units_found"] = units_found
    
    print(f"  Total characters: {analysis['total_chars']}")
    print(f"  Total lines: {analysis['total_lines']}")
    print(f"  Structure: {', '.join(analysis['structure_pattern'])}")
    print(f"  Has pricing: {analysis['has_dollar_signs']}")
    print(f"  Dollar amounts found: {analysis['dollar_amounts_found']}")
    print(f"  Units found: {analysis['units_found']}")
    print(f"  Categories detected: {', '.join(categories_found[:5])}")
    
    return analysis

def main():
    """Analyze all proposals"""
    proposals_dir = Path(PROPOSALS_PATH)
    
    if not proposals_dir.exists():
        print(f"[ERROR] Directory not found: {PROPOSALS_PATH}")
        return
    
    pdf_files = list(proposals_dir.glob("*.pdf")) + list(proposals_dir.glob("*.PDF"))
    
    if not pdf_files:
        print(f"[ERROR] No PDF files found in {PROPOSALS_PATH}")
        return
    
    print(f"Found {len(pdf_files)} PDF files")
    print("="*80)
    
    all_analyses = []
    
    for pdf_file in pdf_files:
        analysis = analyze_proposal(pdf_file)
        if analysis:
            all_analyses.append(analysis)
    
    # Save results
    output_file = Path(__file__).parent.parent / "docs" / "proposal_analyses.json"
    output_file.parent.mkdir(exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_analyses, f, indent=2, default=str)
    
    print(f"\n{'='*80}")
    print(f"[SAVED] Analysis saved to: {output_file}")
    print("="*80)
    
    # Summary
    print("\nSUMMARY:")
    print("-"*80)
    for analysis in all_analyses:
        print(f"\n{analysis['filename']}:")
        print(f"  Structure: {', '.join(analysis['structure_pattern'])}")
        print(f"  Breakdown Level: {'Detailed' if analysis['units_found'] else 'Simple'}")
        print(f"  Categories: {', '.join(analysis['categories_detected'][:3])}")

if __name__ == "__main__":
    main()

