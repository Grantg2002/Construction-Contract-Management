# Prompt Caching Benefits - GPT-4o

## What Changed

We've upgraded from `gpt-4o-mini` to `gpt-4o` with **prompt caching enabled**.

## Why This Is Better

### 1. **Better Extraction Quality**
- GPT-4o is more capable than GPT-4o-mini
- Better at understanding complex proposal structures
- More accurate extraction of scope items and pricing

### 2. **Cost Savings with Caching**
- **System prompt is cached** after first call
- System prompt tokens: **FREE** after first use (50% discount)
- Only pay for the proposal text (user message) and response

### 3. **Faster Response Times**
- Cached prompts process faster
- Reduced latency for subsequent calls

## Cost Breakdown

### GPT-4o Pricing:
- **Input tokens:** $2.50 per 1M tokens
- **Cached input tokens:** $1.25 per 1M tokens (50% discount)
- **Output tokens:** $10.00 per 1M tokens

### Example: Processing a Proposal

**First Call (No Cache):**
- System prompt: ~200 tokens × $2.50/1M = **$0.0005**
- Proposal text: ~3,000 tokens × $2.50/1M = **$0.0075**
- Response: ~500 tokens × $10.00/1M = **$0.005**
- **Total: ~$0.013**

**Subsequent Calls (With Cache):**
- System prompt: ~200 tokens × $1.25/1M = **$0.00025** (cached, 50% off)
- Proposal text: ~3,000 tokens × $2.50/1M = **$0.0075**
- Response: ~500 tokens × $10.00/1M = **$0.005**
- **Total: ~$0.01275**

**Savings per call: ~$0.00025** (small but adds up!)

## How It Works

1. **First proposal:** System prompt is processed and cached
2. **All subsequent proposals:** System prompt uses cached version
3. **Cache lasts:** Until cache expires (ephemeral cache)

## Monitoring

The API response includes:
- `usage.prompt_tokens` - Total prompt tokens
- `usage.completion_tokens` - Response tokens
- `usage.cached_tokens` - Number of cached tokens (if any)

We track this in the response:
```json
{
  "extraction_cost": 0.01275,
  "token_usage": {
    "prompt_tokens": 3200,
    "completion_tokens": 500,
    "cached_tokens": 200,
    "total_tokens": 3700
  }
}
```

## Benefits Summary

✅ **Better accuracy** - GPT-4o is more capable  
✅ **Cost efficient** - Cached system prompt saves money  
✅ **Faster** - Reduced latency with caching  
✅ **Uniform quality** - Consistent extraction across all proposals  

---

**The system prompt is identical every time, so caching is perfect for this use case!** 🚀

