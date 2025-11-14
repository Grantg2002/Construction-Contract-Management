"""
Handles AI calls and token cost logging for Construction Contract Management
"""
import os
from openai import OpenAI
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client (lazy initialization)
_client = None

def get_openai_client():
    """Get or create OpenAI client"""
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY must be set in environment variables or .env file")
        _client = OpenAI(api_key=api_key)
    return _client


async def extract_proposal_data(raw_text: str) -> Dict[str, Any]:
    """
    Extract structured data from proposal text using OpenAI
    
    Consolidates scope items: If no itemized pricing, store ONE row per category/subcategory
    with full description. If has pricing, store individual rows.
    
    Args:
        raw_text: Extracted text from proposal PDF/Word
        
    Returns:
        Dictionary with extracted proposal data
    """
    client = get_openai_client()
    
    system_prompt = """You are an expert at analyzing construction proposals. Extract structured data and consolidate scope items intelligently.

CONSOLIDATION RULES:
1. If a category/subcategory has NO itemized pricing (just descriptions), create ONE row with:
   - category: Main category name
   - subcategory: Subcategory if present (or null)
   - description: ALL items in that category/subcategory combined into one description
   - is_included: true
   - quantity/unit/unit_price/line_total: null (no pricing breakdown)

2. If a category/subcategory HAS itemized pricing, create individual rows for each priced item.

3. Always extract excluded items separately as a list of strings.

4. Extract company name, proposal date, and total price.

Return valid JSON only."""

    user_prompt = f"""Extract data from this construction proposal:

{raw_text}

Return JSON in this exact format:
{{
  "company_name": "Company Name",
  "proposal_date": "YYYY-MM-DD",
  "total_price": 12345.67,
  "scope_items": [
    {{
      "category": "Metal Framing",
      "subcategory": "Interior Walls",
      "description": "20ga @ Interior Walls, Hard Lids, & Bulkheads",
      "is_included": true,
      "quantity": null,
      "unit": null,
      "unit_price": null,
      "line_total": null
    }},
    {{
      "category": "Drywall",
      "subcategory": "Type X",
      "description": "5/8\" Type X U.N.O.",
      "is_included": true,
      "quantity": null,
      "unit": null,
      "unit_price": null,
      "line_total": null
    }}
  ],
  "excluded_items": [
    "Any Dumpsters",
    "Any Wood Framing",
    "Any Blocking"
  ]
}}"""

    response = get_openai_client().chat.completions.create(
        model="gpt-4o",  # Using GPT-4o with prompt caching support
        messages=[
            {"role": "system", "content": system_prompt},  # This will be cached after first call
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
        cache_control={"type": "ephemeral"}  # Enable prompt caching (caches system prompt)
    )
    
    import json
    extracted_data = json.loads(response.choices[0].message.content)
    
    # Add raw text for reference
    extracted_data["raw_text"] = raw_text
    
    # Calculate token cost (accounting for cached tokens)
    usage = response.usage
    cached_tokens = getattr(usage, 'cached_tokens', 0) if usage else 0
    prompt_tokens = usage.prompt_tokens if usage else 0
    completion_tokens = usage.completion_tokens if usage else 0
    
    token_cost = calculate_token_cost(
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        cached_tokens=cached_tokens,
        model="gpt-4o"
    )
    
    extracted_data["extraction_cost"] = token_cost
    extracted_data["token_usage"] = {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "cached_tokens": cached_tokens,
        "total_tokens": prompt_tokens + completion_tokens
    }
    
    return extracted_data


async def process_proposal(file_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a proposal document using OpenAI (legacy function for compatibility)
    
    Args:
        file_data: Dictionary containing file information and content
        
    Returns:
        Dictionary with processed results and token usage
    """
    # Extract content from file_data
    content = file_data.get("content", "")
    
    # Make OpenAI API call
    response = get_openai_client().chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that analyzes construction contract proposals."
            },
            {
                "role": "user",
                "content": f"Analyze this proposal: {content}"
            }
        ]
    )
    
    # Extract token usage
    usage = response.usage
    token_cost = calculate_token_cost(
        prompt_tokens=usage.prompt_tokens if usage else 0,
        completion_tokens=usage.completion_tokens if usage else 0,
        model="gpt-4"
    )
    
    return {
        "analysis": response.choices[0].message.content,
        "tokens_used": {
            "prompt_tokens": usage.prompt_tokens if usage else 0,
            "completion_tokens": usage.completion_tokens if usage else 0,
            "total_tokens": usage.total_tokens if usage else 0
        },
        "cost": token_cost
    }


def calculate_token_cost(prompt_tokens: int, completion_tokens: int, model: str, cached_tokens: int = 0) -> float:
    """
    Calculate the cost of tokens used based on model pricing
    Accounts for prompt caching (cached tokens are 50% cheaper)
    
    Args:
        prompt_tokens: Number of prompt tokens
        completion_tokens: Number of completion tokens
        model: Model name (e.g., "gpt-4o")
        cached_tokens: Number of cached tokens (from prompt caching)
        
    Returns:
        Cost in USD
    """
    # GPT-4o pricing (as of 2024, adjust as needed)
    pricing = {
        "gpt-4o": {
            "prompt": 2.50 / 1000000,  # $2.50 per 1M tokens
            "prompt_cached": 1.25 / 1000000,  # $1.25 per 1M cached tokens (50% discount)
            "completion": 10.00 / 1000000  # $10.00 per 1M tokens
        },
        "gpt-4": {
            "prompt": 0.03 / 1000,  # $0.03 per 1K tokens
            "completion": 0.06 / 1000  # $0.06 per 1K tokens
        },
        "gpt-4o-mini": {
            "prompt": 0.15 / 1000000,  # $0.15 per 1M tokens
            "completion": 0.60 / 1000000  # $0.60 per 1M tokens
        },
        "gpt-3.5-turbo": {
            "prompt": 0.0015 / 1000,
            "completion": 0.002 / 1000
        }
    }
    
    model_pricing = pricing.get(model, pricing["gpt-4o"])
    
    # Calculate cost: cached tokens get discount, non-cached tokens pay full price
    non_cached_prompt_tokens = max(0, prompt_tokens - cached_tokens)
    
    if cached_tokens > 0 and "prompt_cached" in model_pricing:
        # Use cached pricing for cached tokens
        cached_cost = cached_tokens * model_pricing["prompt_cached"]
        non_cached_cost = non_cached_prompt_tokens * model_pricing["prompt"]
        prompt_cost = cached_cost + non_cached_cost
    else:
        # No caching, use regular pricing
        prompt_cost = prompt_tokens * model_pricing["prompt"]
    
    completion_cost = completion_tokens * model_pricing["completion"]
    total_cost = prompt_cost + completion_cost
    
    return round(total_cost, 6)  # More precision for smaller costs

