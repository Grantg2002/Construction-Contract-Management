# Railway Deployment Guide

## Quick Deploy to Railway

### Step 1: Prepare Your Code

✅ Already done:
- `Procfile` - Tells Railway how to start your app
- `runtime.txt` - Specifies Python version
- `railway.json` - Railway configuration
- CORS updated for production

### Step 2: Push to GitHub

Make sure your code is on GitHub:
```bash
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

### Step 3: Deploy to Railway

1. **Go to [railway.app](https://railway.app)**
2. **Sign up** (use GitHub - easiest)
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your repository**
6. **Railway will auto-detect:**
   - ✅ Python project
   - ✅ `Procfile` found
   - ✅ `requirements.txt` found
   - ✅ Auto-install dependencies

### Step 4: Add Environment Variables

In Railway dashboard, go to your project → Variables tab:

Add these variables:
```
SUPABASE_URL=https://olesfyxldqbtxofkequi.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
OPENAI_API_KEY=your-openai-api-key
FRONTEND_URL=https://your-app.netlify.app
```

### Step 5: Get Your Backend URL

Railway will give you a URL like:
```
https://your-app-name.up.railway.app
```

### Step 6: Update Frontend

In Netlify (after deploying frontend), add environment variable:
```
VITE_API_BASE_URL=https://your-app-name.up.railway.app
```

## Why Railway is Perfect for PDF Processing

### ✅ No Timeout Limits
- Vercel: 10 seconds max
- Railway: No limit (perfect for PDF processing)

### ✅ More Memory
- Vercel: 1GB max
- Railway: 2GB+ available (handles large PDFs)

### ✅ Always Running
- Vercel: Cold starts (slow first request)
- Railway: Always warm (fast every time)

### ✅ Full Python Environment
- All libraries work perfectly
- No restrictions on file processing

## Testing Your Deployment

1. **Backend Health Check:**
   ```
   https://your-app-name.up.railway.app/health
   ```
   Should return: `{"status": "healthy"}`

2. **API Documentation:**
   ```
   https://your-app-name.up.railway.app/docs
   ```
   Interactive API docs - test endpoints here!

3. **Test PDF Upload:**
   - Go to your frontend
   - Upload a proposal PDF
   - Should process successfully

## Troubleshooting

### Backend Not Starting?
- Check Railway logs (in dashboard)
- Verify `Procfile` exists
- Check Python version in `runtime.txt`

### CORS Errors?
- Make sure `FRONTEND_URL` is set in Railway
- Check frontend URL matches exactly

### PDF Processing Fails?
- Check Railway logs
- Verify `pdfplumber` is in `requirements.txt`
- Check file size limits

## Cost

**Free Tier:**
- 500 hours/month
- $5 credit/month
- Perfect for development/testing

**Paid Tier (if needed):**
- $5/month for hobby plan
- Unlimited hours
- More resources

## Next Steps

1. ✅ Deploy backend to Railway
2. ✅ Deploy frontend to Netlify
3. ✅ Update frontend with backend URL
4. ✅ Test end-to-end workflow

Your app will be live and ready to process PDFs! 🚀

