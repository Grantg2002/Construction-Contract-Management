# Render Deployment Guide

## Step-by-Step: Deploy Your FastAPI Backend to Render

### Prerequisites
- ✅ Your code is on GitHub
- ✅ You have a GitHub account
- ✅ You have your API keys ready (Supabase, OpenAI)

---

## Step 1: Create Render Account

1. Go to **[render.com](https://render.com)**
2. Click **"Get Started for Free"**
3. Sign up with **GitHub** (easiest option)
4. Authorize Render to access your GitHub account

---

## Step 2: Create New Web Service

1. In Render dashboard, click **"New +"** button
2. Select **"Web Service"**
3. Connect your GitHub repository:
   - If not connected, click **"Configure account"** and authorize
   - Select your repository: `Construction-Contract-Management`
   - Click **"Connect"**

---

## Step 3: Configure Your Service

Render will auto-detect it's a Python project. Configure these settings:

### Basic Settings:
- **Name:** `construction-contract-api` (or your preferred name)
- **Region:** Choose closest to you (Oregon, Ohio, Frankfurt, etc.)
- **Branch:** `main` (or your default branch)
- **Root Directory:** `backend` ⚠️ **Important!**

### Build & Start:
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

⚠️ **Important:** Make sure Root Directory is set to `backend` since that's where your Python code is!

---

## Step 4: Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"** and add:

```
SUPABASE_URL=https://olesfyxldqbtxofkequi.supabase.co
```

```
SUPABASE_ANON_KEY=your-supabase-anon-key-here
```

```
OPENAI_API_KEY=your-openai-api-key-here
```

```
FRONTEND_URL=https://your-app.netlify.app
```
*(Add this after you deploy your frontend to Netlify)*

---

## Step 5: Choose Plan

- Select **"Free"** plan (750 hours/month - plenty for testing)
- Click **"Create Web Service"**

---

## Step 6: Wait for Deployment

Render will:
1. ✅ Clone your repository
2. ✅ Install Python dependencies
3. ✅ Build your application
4. ✅ Start your FastAPI server

**This takes 2-5 minutes.** Watch the logs to see progress.

---

## Step 7: Get Your Backend URL

Once deployed, Render will give you a URL like:
```
https://construction-contract-api.onrender.com
```

**Save this URL** - you'll need it for your frontend!

---

## Step 8: Test Your Backend

### Health Check:
Visit: `https://your-app.onrender.com/health`
Should return: `{"status": "healthy"}`

### API Documentation:
Visit: `https://your-app.onrender.com/docs`
You'll see interactive API docs - test your endpoints here!

---

## Step 9: Update Frontend (After Netlify Deployment)

When you deploy your frontend to Netlify, add this environment variable:

```
VITE_API_BASE_URL=https://your-app.onrender.com
```

---

## Troubleshooting

### Build Fails?
- Check logs in Render dashboard
- Verify `backend/requirements.txt` exists
- Make sure Root Directory is set to `backend`

### App Won't Start?
- Check logs for errors
- Verify `uvicorn` is in `requirements.txt`
- Check Start Command is correct

### CORS Errors?
- Make sure `FRONTEND_URL` is set in Render
- Check your frontend URL matches exactly (no trailing slash)

### PDF Processing Fails?
- Check Render logs
- Verify `pdfplumber` is in `requirements.txt`
- Check file size limits (Render free tier has limits)

---

## Render Free Tier Limits

- ✅ **750 hours/month** (enough for testing)
- ✅ **512MB RAM** (enough for PDF processing)
- ⚠️ **Spins down after 15 minutes of inactivity** (first request after spin-down takes ~30 seconds)
- ⚠️ **No custom domains** on free tier (but subdomain works fine)

**Upgrade to Starter ($7/month) for:**
- Always-on (no spin-down)
- Custom domain
- More resources

---

## Quick Reference

### Your URLs:
- **Backend API:** `https://your-app.onrender.com`
- **API Docs:** `https://your-app.onrender.com/docs`
- **Health Check:** `https://your-app.onrender.com/health`

### Environment Variables Needed:
```
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-supabase-key
OPENAI_API_KEY=your-openai-key
FRONTEND_URL=your-netlify-url (after frontend deploy)
```

---

## Next Steps

1. ✅ Backend deployed to Render
2. ⏭️ Deploy frontend to Netlify
3. ⏭️ Update frontend with backend URL
4. ⏭️ Test end-to-end workflow

Your backend is now live! 🚀

---

## Using render.yaml (Optional)

If you prefer configuration as code, you can use the `render.yaml` file I created:

1. Make sure `render.yaml` is in your repository root
2. In Render, when creating service, select **"Apply render.yaml"**
3. Render will use the configuration from the file

This is optional - you can also configure everything through the web UI.

