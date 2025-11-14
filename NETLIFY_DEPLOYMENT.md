# Netlify Frontend Deployment Guide

## Build Settings for Your React/Vite Frontend

### ✅ Correct Settings:

1. **Base directory:** `frontend`
   - This tells Netlify where your frontend code is located

2. **Build command:** `npm run build`
   - This builds your React app using Vite
   - Creates optimized production files in `frontend/dist`

3. **Publish directory:** `frontend/dist`
   - This is where Vite outputs the built files
   - Netlify will serve these files

4. **Branch to deploy:** `main` ✅ (already set)

5. **Functions directory:** `netlify/functions` ✅ (default, leave as is)

## Step-by-Step Configuration

### In Netlify Build Settings:

1. **Base directory:**
   - Type: `frontend`

2. **Build command:**
   - Type: `npm run build`

3. **Publish directory:**
   - Type: `frontend/dist`

4. **Click "Deploy site"** or **"Finish"**

## After Deployment

### Add Environment Variables:

Go to **Site settings** → **Environment variables** and add:

```
VITE_SUPABASE_URL=https://olesfyxldqbtxofkequi.supabase.co
```

```
VITE_SUPABASE_ANON_KEY=your-supabase-anon-key
```

```
VITE_API_BASE_URL=https://your-render-app.onrender.com
```
*(Add this after your Render backend is deployed)*

## Important Notes

- ✅ Netlify will automatically run `npm install` in the `frontend` directory
- ✅ Then run `npm run build` to create production files
- ✅ Then serve files from `frontend/dist`
- ✅ Your site will be live at: `https://constructioncontractmgt.netlify.app`

## Troubleshooting

### Build Fails?
- Check that `frontend/package.json` exists
- Verify `npm run build` works locally
- Check Netlify build logs

### Environment Variables Not Working?
- Make sure they start with `VITE_` prefix
- Redeploy after adding variables
- Check browser console for errors

### API Calls Fail?
- Make sure `VITE_API_BASE_URL` is set to your Render backend URL
- Check CORS settings on Render backend
- Verify backend is running

