# Word Document Download Feature

## Overview
Added the ability to download subcontract agreements as Word documents (.docx) directly from the subcontracts table.

## Implementation

### Backend Changes

1. **New File: `backend/word_generator.py`**
   - Converts filled HTML template to Word document format
   - Uses `python-docx` and `BeautifulSoup` to parse HTML and create Word documents
   - Preserves tables, lists, paragraphs, and basic formatting

2. **New Endpoint: `GET /api/subcontracts/{subcontract_id}/download-contract`**
   - Generates contract HTML from template with all placeholders filled
   - Converts HTML to Word document (.docx)
   - Returns Word document as downloadable file
   - Filename format: `{ProjectName}_{CompanyName}_Contract.docx`

3. **Updated: `backend/requirements.txt`**
   - Added `beautifulsoup4==4.12.2` for HTML parsing

### Frontend Changes

1. **Updated: `frontend/src/components/SubcontractsTable.jsx`**
   - Added "Download" column to the table
   - Added download button for each subcontract
   - Shows loading state while generating document
   - Handles file download with proper filename

## How It Works

1. User clicks "Download" button in the subcontracts table
2. Frontend calls `/api/subcontracts/{subcontract_id}/download-contract`
3. Backend:
   - Fetches subcontract data from database
   - Gets project information
   - Retrieves scope items (included/excluded)
   - Generates scope HTML
   - Fills template with all placeholders:
     - Project info (name, address, dates)
     - Architect/Engineer info
     - Subcontractor info (company, address, contact)
     - Proposal date and pricing
     - Scope of work HTML
   - Converts filled HTML to Word document
   - Returns as downloadable file

4. Browser downloads the Word document automatically

## Usage

1. Navigate to a project detail page
2. Find the subcontract in the table
3. Click the "Download" button in the "Download" column
4. Word document will be generated and downloaded

## File Location

The Word document is generated on-demand and sent directly to the browser. It's not stored on the server - generated fresh each time you download.

## Notes

- The Word document preserves the original template structure
- Tables, lists, and formatting are maintained
- Complex HTML formatting may need refinement
- Filename includes project name and company name for easy identification

## Future Enhancements

- Cache generated documents for faster re-downloads
- Store documents in Supabase Storage
- Add document versioning
- Support PDF export option
- Improve HTML to Word conversion fidelity

