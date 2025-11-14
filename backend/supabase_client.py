"""
Supabase connection handler for Construction Contract Management
"""
import os
from supabase import create_client, Client
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

_supabase_client: Optional[Client] = None


def get_supabase_client() -> Client:
    """
    Get or create Supabase client instance (singleton pattern)
    """
    global _supabase_client
    
    if _supabase_client is None:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment variables"
            )
        
        _supabase_client = create_client(supabase_url, supabase_key)
    
    return _supabase_client

