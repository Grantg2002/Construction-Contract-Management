# Fix Netlify Deployment Error

## Problem
Netlify error: `Base directory does not exist: /opt/build/repo/frontend`

## Root Cause
The `frontend` folder exists locally but **is not committed to Git**, so Netlify can't find it when cloning the repository.

## Solution

### Step 1: Add Frontend Files to Git

```bash
# Add frontend files (excluding node_modules and dist)
git add frontend/package.json
git add frontend/vite.config.js
git add frontend/index.html
git add frontend/src/
git add frontend/tailwind.config.js
git add frontend/postcss.config.js
```

### Step 2: Commit and Push

```bash
git commit -m "Add frontend files for Netlify deployment"
git push origin main
```

### Step 3: Retry Netlify Deployment

1. Go back to Netlify dashboard
2. Click **"Retry deploy"**
3. Should work now!

## What Was Wrong

- ✅ Frontend folder exists locally
- ❌ Frontend folder NOT in Git repository
- ❌ Netlify clones repo → no frontend folder → build fails

## After Fix

- ✅ Frontend folder in Git
- ✅ Netlify clones repo → finds frontend folder → build succeeds

## Important: Don't Commit These

Make sure these stay in `.gitignore`:
- `frontend/node_modules/` (too large)
- `frontend/dist/` (build output, regenerated)
- `frontend/.vite/` (cache)

But DO commit:
- `frontend/src/` (your source code)
- `frontend/package.json` (dependencies list)
- `frontend/vite.config.js` (build config)
- `frontend/index.html` (entry point)
