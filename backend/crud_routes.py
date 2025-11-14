"""
CRUD API Routes for Construction Contract Management
Provides full Create, Read, Update, Delete operations for all tables
"""
from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List, Dict, Any
from supabase_client import get_supabase_client
from datetime import datetime
import uuid


def setup_crud_routes(app: FastAPI):
    """Setup CRUD routes for all database tables"""
    
    # ============================================
    # PROJECTS CRUD
    # ============================================
    
    @app.get("/api/projects")
    async def get_projects(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        status: Optional[str] = None
    ):
        """Get all projects with pagination"""
        try:
            supabase = get_supabase_client()
            query = supabase.table("projects").select("*")
            
            if status:
                query = query.eq("status", status)
            
            result = query.order("created_at", desc=True).range(skip, skip + limit - 1).execute()
            return {"data": result.data, "count": len(result.data)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/projects/{project_id}")
    async def get_project(project_id: str):
        """Get single project by ID"""
        try:
            supabase = get_supabase_client()
            result = supabase.table("projects").select("*").eq("id", project_id).single().execute()
            if not result.data:
                raise HTTPException(status_code=404, detail="Project not found")
            return result.data
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.put("/api/projects/{project_id}")
    async def update_project(project_id: str, project_data: Dict[str, Any]):
        """Update project"""
        try:
            supabase = get_supabase_client()
            project_data["updated_at"] = datetime.now().isoformat()
            result = supabase.table("projects").update(project_data).eq("id", project_id).execute()
            if not result.data:
                raise HTTPException(status_code=404, detail="Project not found")
            return {"success": True, "data": result.data[0]}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.delete("/api/projects/{project_id}")
    async def delete_project(project_id: str):
        """Delete project (cascade deletes subcontracts)"""
        try:
            supabase = get_supabase_client()
            result = supabase.table("projects").delete().eq("id", project_id).execute()
            return {"success": True, "message": "Project deleted"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # ============================================
    # SUBCONTRACTS CRUD
    # ============================================
    
    @app.get("/api/projects/{project_id}/subcontracts")
    async def get_subcontracts(project_id: str):
        """Get all subcontracts for a project"""
        try:
            supabase = get_supabase_client()
            result = supabase.table("subcontracts").select("*").eq("project_id", project_id).order("created_at", desc=True).execute()
            return {"data": result.data}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/subcontracts/{subcontract_id}")
    async def get_subcontract(subcontract_id: str):
        """Get single subcontract by ID"""
        try:
            supabase = get_supabase_client()
            result = supabase.table("subcontracts").select("*").eq("id", subcontract_id).single().execute()
            if not result.data:
                raise HTTPException(status_code=404, detail="Subcontract not found")
            return result.data
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.put("/api/subcontracts/{subcontract_id}")
    async def update_subcontract(subcontract_id: str, subcontract_data: Dict[str, Any]):
        """Update subcontract"""
        try:
            supabase = get_supabase_client()
            subcontract_data["updated_at"] = datetime.now().isoformat()
            result = supabase.table("subcontracts").update(subcontract_data).eq("id", subcontract_id).execute()
            if not result.data:
                raise HTTPException(status_code=404, detail="Subcontract not found")
            return {"success": True, "data": result.data[0]}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.delete("/api/subcontracts/{subcontract_id}")
    async def delete_subcontract(subcontract_id: str):
        """Delete subcontract"""
        try:
            supabase = get_supabase_client()
            result = supabase.table("subcontracts").delete().eq("id", subcontract_id).execute()
            return {"success": True, "message": "Subcontract deleted"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # ============================================
    # SCOPE ITEMS CRUD
    # ============================================
    
    @app.get("/api/subcontracts/{subcontract_id}/scope-items")
    async def get_scope_items(subcontract_id: str):
        """Get all scope items for a subcontract"""
        try:
            supabase = get_supabase_client()
            result = supabase.table("scope_items").select("*").eq("subcontract_id", subcontract_id).order("display_order").execute()
            return {"data": result.data}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/api/subcontracts/{subcontract_id}/scope-items")
    async def create_scope_item(subcontract_id: str, scope_item: Dict[str, Any]):
        """Create a new scope item"""
        try:
            supabase = get_supabase_client()
            scope_item["subcontract_id"] = subcontract_id
            result = supabase.table("scope_items").insert(scope_item).execute()
            return {"success": True, "data": result.data[0]}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.put("/api/scope-items/{scope_item_id}")
    async def update_scope_item(scope_item_id: str, scope_item: Dict[str, Any]):
        """Update scope item"""
        try:
            supabase = get_supabase_client()
            scope_item["updated_at"] = datetime.now().isoformat()
            result = supabase.table("scope_items").update(scope_item).eq("id", scope_item_id).execute()
            if not result.data:
                raise HTTPException(status_code=404, detail="Scope item not found")
            return {"success": True, "data": result.data[0]}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.delete("/api/scope-items/{scope_item_id}")
    async def delete_scope_item(scope_item_id: str):
        """Delete scope item"""
        try:
            supabase = get_supabase_client()
            result = supabase.table("scope_items").delete().eq("id", scope_item_id).execute()
            return {"success": True, "message": "Scope item deleted"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # ============================================
    # CHANGE ORDERS CRUD
    # ============================================
    
    @app.get("/api/subcontracts/{subcontract_id}/change-orders")
    async def get_change_orders(subcontract_id: str):
        """Get all change orders for a subcontract"""
        try:
            supabase = get_supabase_client()
            result = supabase.table("change_orders").select("*").eq("subcontract_id", subcontract_id).order("created_at", desc=True).execute()
            return {"data": result.data}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/api/subcontracts/{subcontract_id}/change-orders")
    async def create_change_order(subcontract_id: str, change_order: Dict[str, Any]):
        """Create a new change order and update subcontract amount"""
        try:
            supabase = get_supabase_client()
            
            # Get current subcontract amount
            subcontract = supabase.table("subcontracts").select("current_amount").eq("id", subcontract_id).single().execute()
            current_amount = float(subcontract.data.get("current_amount", 0))
            
            # Add change order amount
            change_amount = float(change_order.get("change_amount", 0))
            new_amount = current_amount + change_amount
            
            # Create change order
            change_order["subcontract_id"] = subcontract_id
            change_order["change_order_date"] = change_order.get("change_order_date", datetime.now().isoformat())
            result = supabase.table("change_orders").insert(change_order).execute()
            
            # Update subcontract amount
            supabase.table("subcontracts").update({"current_amount": new_amount}).eq("id", subcontract_id).execute()
            
            return {"success": True, "data": result.data[0], "new_subcontract_amount": new_amount}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # ============================================
    # INVOICES CRUD
    # ============================================
    
    @app.get("/api/subcontracts/{subcontract_id}/invoices")
    async def get_invoices(subcontract_id: str):
        """Get all invoices for a subcontract"""
        try:
            supabase = get_supabase_client()
            result = supabase.table("invoices").select("*").eq("subcontract_id", subcontract_id).order("invoice_date", desc=True).execute()
            return {"data": result.data}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/api/subcontracts/{subcontract_id}/invoices")
    async def create_invoice(subcontract_id: str, invoice: Dict[str, Any]):
        """Create a new invoice and update subcontract totals"""
        try:
            supabase = get_supabase_client()
            
            invoice["subcontract_id"] = subcontract_id
            invoice["invoice_date"] = invoice.get("invoice_date", datetime.now().isoformat())
            result = supabase.table("invoices").insert(invoice).execute()
            
            # Update subcontract total_billed
            invoices = supabase.table("invoices").select("invoice_amount").eq("subcontract_id", subcontract_id).execute()
            total_billed = sum(float(inv.get("invoice_amount", 0)) for inv in invoices.data)
            supabase.table("subcontracts").update({"total_billed": total_billed}).eq("id", subcontract_id).execute()
            
            return {"success": True, "data": result.data[0], "total_billed": total_billed}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # ============================================
    # PAYMENTS CRUD
    # ============================================
    
    @app.get("/api/invoices/{invoice_id}/payments")
    async def get_payments(invoice_id: str):
        """Get all payments for an invoice"""
        try:
            supabase = get_supabase_client()
            result = supabase.table("payments").select("*").eq("invoice_id", invoice_id).order("payment_date", desc=True).execute()
            return {"data": result.data}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/api/invoices/{invoice_id}/payments")
    async def create_payment(invoice_id: str, payment: Dict[str, Any]):
        """Create a new payment"""
        try:
            supabase = get_supabase_client()
            payment["invoice_id"] = invoice_id
            payment["payment_date"] = payment.get("payment_date", datetime.now().isoformat())
            result = supabase.table("payments").insert(payment).execute()
            return {"success": True, "data": result.data[0]}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

