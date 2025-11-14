# Render Settings Checklist

## ✅ Correct Settings for Your FastAPI Backend

### 1. Name ✅
- **Current:** `Construction-Contract-Management`
- **Status:** ✅ Good (or use `construction-contract-api`)

### 2. Language ❌ NEEDS CHANGE
- **Current:** `Ruby` ❌
- **Should be:** `Python 3` ✅
- **Action:** Change dropdown to "Python 3"

### 3. Branch ✅
- **Current:** `main`
- **Status:** ✅ Good

### 4. Region ✅
- **Current:** `Oregon (US West)`
- **Status:** ✅ Good (or choose closest to you)

### 5. Root Directory ❌ NEEDS CHANGE
- **Current:** Empty ❌
- **Should be:** `backend` ✅
- **Action:** Type `backend` in the field
- **Why:** Your Python code is in the `backend/` folder

### 6. Build Command ❌ NEEDS CHANGE
- **Current:** `$ bundle install` ❌ (Ruby command)
- **Should be:** `pip install -r requirements.txt` ✅
- **Action:** Replace with Python command

### 7. Start Command ❌ NEEDS CHANGE
- **Current:** `$ bundle exec puma` ❌ (Ruby command)
- **Should be:** `uvicorn main:app --host 0.0.0.0 --port $PORT` ✅
- **Action:** Replace with FastAPI command

## Step-by-Step Fix

1. **Change Language:**
   - Click the "Language" dropdown
   - Select **"Python 3"**

2. **Set Root Directory:**
   - In "Root Directory" field, type: `backend`

3. **Update Build Command:**
   - Replace `$ bundle install` with: `pip install -r requirements.txt`

4. **Update Start Command:**
   - Replace `$ bundle exec puma` with: `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Click "Create Web Service"** or **"Save Changes"**

## After Creating Service

Don't forget to add Environment Variables:
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `OPENAI_API_KEY`
- `FRONTEND_URL` (add after frontend deploy)

