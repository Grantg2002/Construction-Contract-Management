# Deployment Guide

## Overview

Your app has two parts:
1. **Frontend (React)** → Deploy to Netlify ✅
2. **Backend (FastAPI)** → Deploy to Railway/Render

## Frontend Deployment (Netlify)

### Step 1: Build Frontend
```bash
cd frontend
npm run build
```

### Step 2: Deploy to Netlify
1. Go to [netlify.com](https://netlify.com)
2. Sign up/login
3. Click "Add new site" → "Deploy manually"
4. Drag the `frontend/dist` folder
5. Add environment variables:
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`
   - `VITE_API_BASE_URL` (your backend URL)

### Step 3: Update API URL
After deploying backend, update `VITE_API_BASE_URL` in Netlify to point to your backend URL.

## Backend Deployment (Railway - Recommended)

### Step 1: Prepare for Deployment

Create `Procfile` in backend directory:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

Create `runtime.txt`:
```
python-3.11
```

### Step 2: Deploy to Railway
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Select your repository
6. Railway will auto-detect Python
7. Add environment variables:
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
   - `OPENAI_API_KEY`
8. Deploy!

### Step 3: Get Backend URL
Railway will give you a URL like: `https://your-app.railway.app`

## Backend Deployment (Render - Alternative)

### Step 1: Create `render.yaml`
```yaml
services:
  - type: web
    name: construction-contract-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: SUPABASE_URL
        sync: false
      - key: SUPABASE_ANON_KEY
        sync: false
      - key: OPENAI_API_KEY
        sync: false
```

### Step 2: Deploy to Render
1. Go to [render.com](https://render.com)
2. Sign up
3. Click "New Web Service"
4. Connect GitHub repo
5. Select backend directory
6. Add environment variables
7. Deploy!

## Environment Variables

### Backend (.env)
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
OPENAI_API_KEY=your-openai-key
```

### Frontend (Netlify Environment Variables)
```
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
VITE_API_BASE_URL=https://your-backend.railway.app
```

## CORS Configuration

Update `backend/main.py` to allow your frontend domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Local dev
        "https://your-app.netlify.app",  # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Testing Deployment

1. **Frontend:** Visit your Netlify URL
2. **Backend:** Visit `https://your-backend.railway.app/docs` to see API docs
3. **Health Check:** `https://your-backend.railway.app/health`

## Cost Estimate

- **Netlify:** Free (frontend hosting)
- **Railway:** Free tier (500 hours/month), then $5/month
- **Render:** Free tier (750 hours/month), then $7/month
- **Supabase:** Free tier (database)
- **OpenAI:** Pay per use (~$0.01-0.10 per proposal)

**Total:** $0-12/month depending on usage

