"""
Proposal Extraction Service
Extracts information from PDF/Word proposals and consolidates scope items
"""
import pdfplumber
from docx import Document
from openai_handler import extract_proposal_data
from typing import Dict, List, Optional
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


def extract_text_from_docx(file_content: bytes) -> str:
    """Extract text from Word document"""
    try:
        doc = Document(io.BytesIO(file_content))
        text_parts = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text_parts.append(paragraph.text)
        return "\n\n".join(text_parts)
    except Exception as e:
        raise Exception(f"Error extracting Word text: {str(e)}")


def extract_text_from_file(file_content: bytes, filename: str) -> str:
    """Extract text from file based on extension"""
    filename_lower = filename.lower()
    
    if filename_lower.endswith('.pdf'):
        return extract_text_from_pdf(file_content)
    elif filename_lower.endswith(('.doc', '.docx')):
        return extract_text_from_docx(file_content)
    else:
        raise ValueError(f"Unsupported file type: {filename}")


async def process_proposal_file(file_content: bytes, filename: str) -> Dict:
    """
    Process a proposal file and extract structured data
    
    Returns:
        {
            'company_name': str,
            'proposal_date': str (YYYY-MM-DD),
            'total_price': float,
            'scope_items': [
                {
                    'category': str,
                    'subcategory': Optional[str],
                    'description': str,  # Full consolidated description
                    'is_included': bool,
                    'quantity': Optional[float],
                    'unit': Optional[str],
                    'unit_price': Optional[float],
                    'line_total': Optional[float]
                }
            ],
            'excluded_items': [str],  # List of excluded items
            'raw_text': str
        }
    """
    # Extract text from file
    raw_text = extract_text_from_file(file_content, filename)
    
    # Use AI to extract and consolidate data
    extracted_data = await extract_proposal_data(raw_text)
    
    return extracted_data

