"""
FastAPI backend entry point for Construction Contract Management
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api_routes import setup_routes
from crud_routes import setup_crud_routes

app = FastAPI(title="Construction Contract Management API")

# CORS configuration
# Allow both local development and production frontend
allowed_origins = [
    "http://localhost:5173",  # Local Vite dev server
    "http://localhost:3000",  # Alternative local port
]

# Add production frontend URL from environment variable if set
import os
production_frontend = os.getenv("FRONTEND_URL")
if production_frontend:
    allowed_origins.append(production_frontend)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup all routes
setup_routes(app)  # Complex operations (proposals, AI, Word generation)
setup_crud_routes(app)  # Full CRUD operations for all tables


@app.get("/")
async def root():
    return {"message": "Construction Contract Management API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

