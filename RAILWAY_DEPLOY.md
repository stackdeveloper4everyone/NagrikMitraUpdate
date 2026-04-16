# Railway.app Backend Deployment (Free & Easy)

## Step 1: Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub (free)
3. Connect your GitHub account

## Step 2: Deploy Backend
1. Click **"New Project"** → **"Deploy from GitHub repo"**
2. Select your repository: `stackdeveloper4everyone/NagrikMitraUpdate`
3. Railway will auto-detect Python and create the service

## Step 3: Configure Environment Variables
In your Railway project settings, add these variables:

```
SARVAM_API_KEY=sk_3nzrcf5o_YNKxePmDmPcAgFUUELkgwcmX
TAVILY_API_KEY=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
LOG_LEVEL=INFO
```

## Step 4: Get Your Backend URL
After deployment, Railway will give you a URL like:
`https://nagrikmitra-production.up.railway.app`

## Step 5: Update Streamlit Secrets
In your Streamlit Cloud app settings → Secrets, update:
```toml
API_BASE_URL = "https://your-railway-url.up.railway.app"
```

## That's it! Your app will work end-to-end.

---

## Alternative: Deploy to Fly.io (Also Free)

If Railway doesn't work:

1. Go to https://fly.io
2. `fly launch` in your terminal
3. `fly deploy`

---

## Quick Test: Make Frontend Work Without Backend

If you want to deploy frontend first, I can modify it to show a demo mode.