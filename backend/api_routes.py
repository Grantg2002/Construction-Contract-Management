"""
API Routes for Construction Contract Management
"""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, Response
from typing import Optional
import base64
from proposal_extractor import process_proposal_file
from scope_html_generator import generate_scope_html
from template_filler import generate_contract_html
from word_generator import html_to_word
from supabase_client import get_supabase_client
from schedule_extractor import extract_schedules_from_drawing, format_schedule_for_database
import uuid
from datetime import datetime


def setup_routes(app: FastAPI):
    """Setup all API routes"""
    
    def get_project_uuid(project_identifier: str) -> str:
        """
        Get project UUID from either UUID or project name
        Returns the UUID if found, raises HTTPException if not
        """
        supabase = get_supabase_client()
        
        # Check if it's already a valid UUID
        try:
            uuid.UUID(project_identifier)
            # It's a valid UUID, verify it exists
            result = supabase.table("projects").select("id").eq("id", project_identifier).single().execute()
            if result.data:
                return project_identifier
            else:
                raise HTTPException(status_code=404, detail=f"Project with UUID {project_identifier} not found")
        except ValueError:
            # Not a UUID, try to find by name
            result = supabase.table("projects").select("id").eq("name", project_identifier).single().execute()
            if result.data and result.data.get("id"):
                return result.data["id"]
            else:
                raise HTTPException(status_code=404, detail=f"Project '{project_identifier}' not found")
    
    @app.post("/api/projects/{project_id}/drawings")
    async def upload_drawing(
        project_id: str,
        file: UploadFile = File(...),
        drawing_type: str = Form(...),  # "architectural" or "engineering"
        drawing_date: str = Form(...),  # YYYY-MM-DD
        architect_name: Optional[str] = Form(None),  # Required for architectural drawings
        engineer_name: Optional[str] = Form(None),  # Required for engineering drawings
        revision_number: Optional[str] = Form(None),
        notes: Optional[str] = Form(None)
    ):
        """Upload architectural or engineering drawing
        
        project_id can be either:
        - A UUID (e.g., "123e4567-e89b-12d3-a456-426614174000")
        - A project name (e.g., "Serveone_Buildout")
        
        For architectural drawings: architect_name is required
        For engineering drawings: engineer_name is required
        
        When you upload a new revision, it will automatically update the project's
        drawing dates and architect/engineer info.
        """
        try:
            supabase = get_supabase_client()
            
            # Get actual UUID (handles both UUID and project name)
            actual_project_uuid = get_project_uuid(project_id)
            
            # Validate required fields based on drawing type
            if drawing_type == "architectural" and not architect_name:
                raise HTTPException(
                    status_code=400, 
                    detail="architect_name is required for architectural drawings"
                )
            if drawing_type == "engineering" and not engineer_name:
                raise HTTPException(
                    status_code=400, 
                    detail="engineer_name is required for engineering drawings"
                )
            
            # Read file content
            file_content = await file.read()
            file_size = len(file_content)
            
            # Upload to Supabase Storage (or store locally for now)
            # For MVP, we'll store file info and you can implement storage later
            file_url = f"drawings/{actual_project_uuid}/{file.filename}"  # Placeholder
            
            # Insert drawing record
            drawing_data = {
                "project_id": actual_project_uuid,
                "drawing_type": drawing_type,
                "drawing_date": drawing_date,
                "revision_number": revision_number,
                "file_name": file.filename,
                "file_size": file_size,
                "file_url": file_url,
                "architect_name": architect_name,
                "engineer_name": engineer_name,
                "notes": notes,
                "is_current": True  # This will trigger the database trigger to update project dates
            }
            
            result = supabase.table("drawings").insert(drawing_data).execute()
            drawing_id = result.data[0]["id"]
            
            return {
                "success": True,
                "drawing_id": drawing_id,
                "message": "Drawing uploaded successfully. Project drawing dates have been updated.",
                "drawing": {
                    "id": drawing_id,
                    "type": drawing_type,
                    "date": drawing_date,
                    "architect": architect_name,
                    "engineer": engineer_name
                }
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    
    @app.post("/api/projects/{project_id}/proposals")
    async def upload_proposal(
        project_id: str,
        file: UploadFile = File(...)
    ):
        """Upload and process a proposal
        
        project_id can be either:
        - A UUID (e.g., "123e4567-e89b-12d3-a456-426614174000")
        - A project name (e.g., "Serveone_Buildout")
        """
        try:
            # Get actual UUID (handles both UUID and project name)
            actual_project_uuid = get_project_uuid(project_id)
            
            # Read file
            file_content = await file.read()
            
            # Extract proposal data
            extracted_data = await process_proposal_file(file_content, file.filename)
            
            # Generate scope HTML
            scope_html = generate_scope_html(
                extracted_data.get("scope_items", []),
                extracted_data.get("excluded_items", [])
            )
            
            # Store proposal in database
            supabase = get_supabase_client()
            
            # Create subcontract record
            subcontract_data = {
                "project_id": actual_project_uuid,
                "company_name": extracted_data.get("company_name", ""),
                "proposal_date": extracted_data.get("proposal_date"),
                "original_amount": extracted_data.get("total_price", 0),
                "current_amount": extracted_data.get("total_price", 0),
                "scope_of_work_html": scope_html,
                "status": "draft"
            }
            
            subcontract_result = supabase.table("subcontracts").insert(subcontract_data).execute()
            subcontract_id = subcontract_result.data[0]["id"]
            
            # Store scope items
            scope_items = extracted_data.get("scope_items", [])
            if scope_items:
                items_to_insert = []
                for idx, item in enumerate(scope_items):
                    items_to_insert.append({
                        "subcontract_id": subcontract_id,
                        "item_number": idx + 1,
                        "category": item.get("category"),
                        "subcategory": item.get("subcategory"),
                        "description": item.get("description"),
                        "is_included": item.get("is_included", True),
                        "quantity": item.get("quantity"),
                        "unit": item.get("unit"),
                        "unit_price": item.get("unit_price"),
                        "line_total": item.get("line_total"),
                        "display_order": idx + 1
                    })
                
                supabase.table("scope_items").insert(items_to_insert).execute()
            
            # Store excluded items as scope items with is_included=false
            excluded_items = extracted_data.get("excluded_items", [])
            if excluded_items:
                excluded_to_insert = []
                start_idx = len(scope_items)
                for idx, excluded in enumerate(excluded_items):
                    excluded_to_insert.append({
                        "subcontract_id": subcontract_id,
                        "item_number": start_idx + idx + 1,
                        "category": "Excluded",
                        "description": excluded,
                        "is_included": False,
                        "display_order": start_idx + idx + 1
                    })
                
                supabase.table("scope_items").insert(excluded_to_insert).execute()
            
            return {
                "success": True,
                "subcontract_id": subcontract_id,
                "extracted_data": extracted_data,
                "scope_html": scope_html,
                "extraction_cost": extracted_data.get("extraction_cost", 0)
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    
    @app.post("/api/subcontracts/{subcontract_id}/generate-contract")
    async def generate_contract(
        subcontract_id: str,
        subcontractor_data: dict  # JSON body with company info
    ):
        """Generate contract HTML from template"""
        try:
            supabase = get_supabase_client()
            
            # Get subcontract data
            subcontract_result = supabase.table("subcontracts")\
                .select("*")\
                .eq("id", subcontract_id)\
                .single()\
                .execute()
            
            subcontract = subcontract_result.data
            project_id = subcontract["project_id"]
            
            # Get scope items
            scope_items_result = supabase.table("scope_items")\
                .select("*")\
                .eq("subcontract_id", subcontract_id)\
                .order("display_order")\
                .execute()
            
            scope_items = scope_items_result.data
            
            # Separate included and excluded
            included_items = [item for item in scope_items if item.get("is_included", True)]
            excluded_items = [item["description"] for item in scope_items if not item.get("is_included", True)]
            
            # Generate scope HTML
            scope_html = generate_scope_html(included_items, excluded_items)
            
            # Generate contract HTML
            contract_html = await generate_contract_html(
                project_id=project_id,
                subcontractor_data=subcontractor_data,
                scope_html=scope_html,
                proposal_date=subcontract.get("proposal_date", ""),
                total_price=float(subcontract.get("current_amount", 0))
            )
            
            # Update subcontract with generated HTML
            supabase.table("subcontracts")\
                .update({"scope_of_work_html": scope_html})\
                .eq("id", subcontract_id)\
                .execute()
            
            return {
                "success": True,
                "contract_html": contract_html
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    
    @app.get("/api/subcontracts/{subcontract_id}/download-contract")
    async def download_contract(subcontract_id: str):
        """Generate and download contract as Word document"""
        try:
            supabase = get_supabase_client()
            
            # Get subcontract data
            subcontract_result = supabase.table("subcontracts")\
                .select("*")\
                .eq("id", subcontract_id)\
                .single()\
                .execute()
            
            if not subcontract_result.data:
                raise HTTPException(status_code=404, detail="Subcontract not found")
            
            subcontract = subcontract_result.data
            project_id = subcontract["project_id"]
            
            # Get project to get company name for filename
            project_result = supabase.table("projects")\
                .select("name")\
                .eq("id", project_id)\
                .single()\
                .execute()
            project_name = project_result.data.get("name", "Project") if project_result.data else "Project"
            
            # Get scope items
            scope_items_result = supabase.table("scope_items")\
                .select("*")\
                .eq("subcontract_id", subcontract_id)\
                .order("display_order")\
                .execute()
            
            scope_items = scope_items_result.data if scope_items_result.data else []
            
            # Separate included and excluded
            included_items = [item for item in scope_items if item.get("is_included", True)]
            excluded_items = [item["description"] for item in scope_items if not item.get("is_included", True)]
            
            # Generate scope HTML
            scope_html = generate_scope_html(included_items, excluded_items)
            
            # Get subcontractor data from database
            subcontractor_data = {
                "company_name": subcontract.get("company_name", ""),
                "street": subcontract.get("subcontractor_street", ""),
                "city": subcontract.get("subcontractor_city", ""),
                "state": subcontract.get("subcontractor_state", ""),
                "zip": subcontract.get("subcontractor_zip", ""),
                "email": subcontract.get("subcontractor_email", ""),
                "phone": subcontract.get("subcontractor_phone", ""),
                "fax": subcontract.get("subcontractor_fax", ""),
                "representative_name": subcontract.get("representative_name", "")
            }
            
            # Generate contract HTML
            contract_html = await generate_contract_html(
                project_id=project_id,
                subcontractor_data=subcontractor_data,
                scope_html=scope_html,
                proposal_date=subcontract.get("proposal_date", ""),
                total_price=float(subcontract.get("current_amount", 0))
            )
            
            # Convert HTML to Word document
            word_bytes = html_to_word(contract_html)
            
            # Generate filename
            company_name_clean = subcontractor_data["company_name"].replace(" ", "_").replace("/", "-")[:30]
            filename = f"{project_name}_{company_name_clean}_Contract.docx"
            
            # Return Word document as download
            return Response(
                content=word_bytes,
                media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                headers={
                    "Content-Disposition": f'attachment; filename="{filename}"'
                }
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    
    @app.get("/api/projects/{project_id}/drawings")
    async def get_project_drawings(project_id: str):
        """Get all drawings for a project
        
        project_id can be either:
        - A UUID (e.g., "123e4567-e89b-12d3-a456-426614174000")
        - A project name (e.g., "Serveone_Buildout")
        """
        try:
            # Get actual UUID (handles both UUID and project name)
            actual_project_uuid = get_project_uuid(project_id)
            
            supabase = get_supabase_client()
            
            result = supabase.table("drawings")\
                .select("*")\
                .eq("project_id", actual_project_uuid)\
                .order("drawing_date", desc=True)\
                .execute()
            
            return {
                "success": True,
                "drawings": result.data
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    
    @app.patch("/api/drawings/{drawing_id}")
    async def update_drawing_metadata(
        drawing_id: str,
        drawing_date: Optional[str] = None,
        architect_name: Optional[str] = None,
        engineer_name: Optional[str] = None,
        revision_number: Optional[str] = None,
        notes: Optional[str] = None
    ):
        """Update drawing metadata (date, architect, engineer, etc.)"""
        try:
            supabase = get_supabase_client()
            
            # Build update dict (only include provided fields)
            update_data = {}
            if drawing_date is not None:
                update_data["drawing_date"] = drawing_date
            if architect_name is not None:
                update_data["architect_name"] = architect_name
            if engineer_name is not None:
                update_data["engineer_name"] = engineer_name
            if revision_number is not None:
                update_data["revision_number"] = revision_number
            if notes is not None:
                update_data["notes"] = notes
            
            if not update_data:
                raise HTTPException(status_code=400, detail="No fields provided to update")
            
            result = supabase.table("drawings")\
                .update(update_data)\
                .eq("id", drawing_id)\
                .execute()
            
            if not result.data:
                raise HTTPException(status_code=404, detail="Drawing not found")
            
            return {
                "success": True,
                "drawing": result.data[0],
                "message": "Drawing metadata updated successfully"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    
    @app.get("/api/drawings/{drawing_id}/schedules")
    async def get_drawing_schedules(drawing_id: str):
        """Get all schedules extracted from a drawing"""
        try:
            supabase = get_supabase_client()
            
            result = supabase.table("drawing_schedules")\
                .select("*")\
                .eq("drawing_id", drawing_id)\
                .order("schedule_type")\
                .order("item_designation")\
                .execute()
            
            return {
                "success": True,
                "schedules": result.data,
                "count": len(result.data) if result.data else 0
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    
    @app.get("/api/projects/{project_id}/schedules")
    async def get_project_schedules(project_id: str):
        """Get all schedules for a project (from all drawings)"""
        try:
            # Get actual UUID (handles both UUID and project name)
            actual_project_uuid = get_project_uuid(project_id)
            
            supabase = get_supabase_client()
            
            result = supabase.table("drawing_schedules")\
                .select("*")\
                .eq("project_id", actual_project_uuid)\
                .order("schedule_type")\
                .order("item_designation")\
                .execute()
            
            # Group by schedule type
            schedules_by_type = {
                "doors": [],
                "windows": [],
                "floors": [],
                "ceilings": [],
                "paint": []
            }
            
            if result.data:
                for item in result.data:
                    schedule_type = item.get("schedule_type")
                    if schedule_type in schedules_by_type:
                        schedules_by_type[schedule_type].append(item)
            
            return {
                "success": True,
                "schedules": schedules_by_type,
                "total_count": len(result.data) if result.data else 0
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

